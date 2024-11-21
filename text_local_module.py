#
#
def replace_dict_func(language : str = ""):
        if language.lower() == "it":
            return {"all":"al", "dell":"del", "l":"lo", "sull":"su","nell":"in","d":"di","c":"ci","s":"si","t":"ti","vent":"venti"}
        else:
            return dict({})
#
#
class text_analyzer:
    #    
    #Initialization
    def __init__ (self, text : str, language = None, *,verbose : bool = True):
        #
        #Initializing the hidden attributes
        ##Read-only attribute
        self._text_raw = text
        ##Read-write attribute
        self.verbose = verbose
        self.language = language
        global re
        if "re" not in globals():
            if self.verbose:
                print("I need the RegEx library. I'm executing 'import re'.")
            import re
        #
        #Initializing the hidden attributes
        self.__text_processed         = None
        self.__text_splitted          = None #Needs __text_processed
        self.__text_counted           = None #Needs __text_splitted
        self.__text_counted_dataframe = None #Needs __text_splitted
        self.__text_lemmatized        = None #Needs __text_counted
        self.__text_lemma_counted     = None #Needs __text_lemmatized
        self.__language_used          = self.language 
        #
        self._languages = ['ast', 'bg', 'ca', 'cs', 'cy', 'da', 'de', 'el', 'en', 'enm', 'es', 'et', 'fa', 
                                'fi', 'fr', 'ga', 'gd', 'gl', 'gv', 'hbs', 'hi', 'hu', 'hy', 'id', 'is', 'it', 
                                'ka', 'la', 'lb', 'lt', 'lv', 'mk', 'ms', 'nb', 'nl', 'nn', 'pl', 'pt', 'ro', 
                                'ru', 'se', 'sk', 'sl', 'sq', 'sv', 'sw', 'tl', 'tr', 'uk']
    #
    #Retrieve the raw text without allowing for changes
    @property
    def text_raw(self):
        return self._text_raw
    @text_raw.setter
    def text_raw(self, value):
        raise AttributeError("WARNING: The initial raw test is read-only and cannot be modified.")
    #
    #Retrieve the list of available languages
    @property
    def languages(self):
        return self._languages
    @languages.setter
    def languages(self, value):
        raise AttributeError("WARNING: The list of available languages is read-only and cannot be modified.")
    #
    #A method to check if an attribute has already been defined
    def __none_check(self,variable):
        return type(variable) == type(None)
    #
    #A function to import the simplemma library, only if it has not been importe before
    def __import_simplemma(self):
        global simplemma
        if "simplemma" not in globals():
            if self.verbose:
                print("I need a lemmatization library. I'm executing 'import simplemma'.")
            try:
                import simplemma
            except Exception as exc:
                print("ERROR: Error while importing the simplemma library.\nI cannot lemmatize the words.\nError code: ", exc)
                return True
        return False
    #
    #A function to import the pandas library, only if it has not been importe before
    def __import_pandas(self):
        global pd
        if "pd" not in globals():
            if self.verbose:
                print("I need pandas. I'm executing 'import pandas as pd'.")
            try:
                import pandas as pd
            except Exception as exc:
                print("ERROR: Error while importing the pandas library.\nI cannot lemmatize the words.\nError code: ", exc)
                return True
        return False
    #
    def text_process(self):
        #
        if self.__none_check(self.__text_processed):
            if self.verbose:
                print("Please wait: "+"I am processing the text.")
            self.__text_processed = self._text_raw.lower()
            #
            puntuaction_list = set(re.findall(r"\W", self.__text_processed))-{" "}
            self.__text_processed = self.__text_processed.replace("'"," ")
            #
            typos_set = set({})
            for puntuaction in puntuaction_list:
                typos_set |= set(re.findall(rf"\{puntuaction}\S", self.__text_processed))
            #
            for typos in typos_set:
                self.__text_processed = self.__text_processed.replace(typos," "+typos[1])
            #
            for puntuaction in puntuaction_list:
                self.__text_processed = self.__text_processed.replace(puntuaction,"")
            #
            self.__text_processed = re.sub(r'\s+', ' ', self.__text_processed)
            self.__text_processed = self.__text_processed.strip()
            #
        return self.__text_processed
    #
    def words_split(self):
        if self.__none_check(self.__text_processed):
            self.text_process()
        #
        if self.__none_check(self.__text_splitted):
            if self.verbose:
                print("Please wait: "+"I am splitting the words.")
            self.__text_splitted = re.split(r" |'", self.__text_processed)
            #self.__text_splitted = list(filter(lambda x: x != "", self.__text_splitted))
            self.__text_splitted = [item for item in self.__text_splitted if (not item.isdigit()) and item!=""]
        #
        return self.__text_splitted
    #   
    def word_count(self,key_word = None, *, dict = False): 
        #
        if self.__import_pandas():
            return None
        #
        if self.__none_check(self.__text_splitted):
            self.words_split()
        # 
        if self.__none_check(self.__text_counted):
            if self.verbose: 
                print("Please wait: "+"I am counting the words.")
            splitted_text = self.__text_splitted
            final_dict = {}
            for word in set(splitted_text):
                final_dict.update({word:splitted_text.count(word)})
            self.__text_counted = final_dict
            self.__text_counted_dataframe = pd.DataFrame({"Raw" : final_dict.keys(), "Raw Count" : final_dict.values()})
        #
        if key_word == None:
            if dict:
                return self.__text_counted
            else:
                return self.__text_counted_dataframe
        else:
            if key_word in self.__text_counted.keys():
                return self.__text_counted[key_word]
            else:
                return 0
    #        
    def lemmatize(self):
        #
        if self.__import_simplemma():
            return None
        if self.__import_pandas():
            return None
        #
        if self.__none_check(self.__text_counted):
            self.word_count()  
        #
        if type(self.language)==type(None):
            if self.verbose:
                print("WARNING: no language is specified, I'll try to detect the language.")
            max_score = 0.0
            language_guess = ''
            text_length = min(3*(10**3), len(self._text_raw))
            for my_lang in self._languages:
                
                score = simplemma.in_target_language(self._text_raw[0:text_length], lang = my_lang)
                if score>max_score:
                    max_score = score
                    language_guess = my_lang
            print(f"WARNING: the language detected is {language_guess}, with confidence {max_score} (between 0 and 1)")
            self.language = language_guess
            self.__language_used = language_guess
        #
        language_check = (self.__language_used != self.language)
        #
        if self.__none_check(self.__text_lemmatized) or language_check:
            if self.verbose:
                if not language_check:
                    print("Please wait: "+"I am lemmatizing the text.") 
                else:
                    print("Please wait: "+"I am lemmatizing again the text with the new language.") 
            #
            self.__text_lemmatized = dict(self.__text_counted)
            words_list = self.__text_lemmatized.keys()
            #
            self.__language_used = self.language
            #
            repl_dict = replace_dict_func(self.language)
            if repl_dict != dict({}):
                for old_word in list(words_list):
                    new_word = repl_dict.get(old_word, old_word)
                    self.__text_lemmatized[new_word] = self.__text_lemmatized.pop(old_word)
            #
            words_list_lemmatized = []
            words_list_count = []
            for word in words_list:
                words_list_lemmatized.append(simplemma.lemmatize(word, lang=self.language))
                words_list_count.append(self.__text_lemmatized[word])
            #
            self.__text_lemmatized = pd.DataFrame({
                "Raw": list(words_list),
                "Lemma": words_list_lemmatized,
                "Raw Count": words_list_count
                })
        #
        return self.__text_lemmatized    
    #   
    def lemma_count(self):
        #
        if self.__none_check(self.__text_lemmatized) or self.__language_used != self.language:
            self.lemmatize(self, self.language)
        #
        if self.__none_check(self.__text_lemma_counted):
            if self.verbose:
                print("Please wait: "+"I am counting the lemmas.")
            lemma_occurrences = self.__text_lemmatized.groupby("Lemma")["Raw"].unique().reset_index()
            lemma_occurrences.columns = ['Lemma', 'Occurrences']
            lemma_counts = self.__text_lemmatized.groupby("Lemma")["Raw Count"].sum().reset_index()
            lemma_counts.columns = ['Lemma', 'Lemma Count']
            self.__text_lemma_counted = lemma_counts.merge(lemma_occurrences, on = "Lemma")    
        #       
        return self.__text_lemma_counted 
    #
    def word_count_print(self,word:str = None):
        if self.__none_check(word):
            display(self.word_count())
        else:
            if type(word)!=str:
                print("WARNING: The word mut be a string.")
            else:
                print("The word '"+word+"' occurs",self.word_count(word),"times.")