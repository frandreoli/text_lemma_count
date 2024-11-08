def replace_dict_func(language : str = ""):
        if language.lower() == "it":
            return {"all":"al", "dell":"del", "l":"lo", "sull":"su","nell":"in"}
        else:
            return dict({})


class text_analyzer:
    #    
    def __init__ (self, text : str, verbose : bool = True):
        self._text_raw = text
        self.verbose = verbose
        global re
        if "re" not in globals():
            if self.verbose:
                print("I need the RegEx library. I'm executing 'import re'.")
            import re
        #
        self.__text_processed     = None
        self.__text_splitted      = None #Needs __text_processed
        self.__text_counted       = None #Needs __text_splitted
        self.__text_lemmatized    = None #Needs __text_counted
        self.__text_lemma_counted = None #Needs __text_lemmatized
    #
    #Retrieve the raw text without allowng for changes
    @property
    def text_raw(self):
        return self._text
    @text_raw.setter
    def text_raw(self, value):
        raise AttributeError("The raw test that is initialized is read-only and cannot be modified.")
    #
    def __none_check(self,variable):
        return type(variable) == type(None)
    #
    def text_process(self):
        #
        if self.__none_check(self.__text_processed):
            if self.verbose:
                print("I am processing the text. Please wait.")
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
            #
        return self.__text_processed
    #
    def words_split(self):
        if self.__none_check(self.__text_processed):
            self.text_process()
        #
        if self.__none_check(self.__text_splitted):
            if self.verbose:
                print("I am splitting the words. Please wait.")
            self.__text_splitted = re.split(r" |'", self.__text_processed)
        #
        return self.__text_splitted
    #   
    def word_count(self,key_word = None): 
        #
        if self.__none_check(self.__text_splitted):
            self.words_split()
        # 
        if self.__none_check(self.__text_counted):
            if self.verbose: 
                print("I am counting the words. Please wait.")
            splitted_text = self.__text_splitted
            final_dict = {}
            for word in set(splitted_text):
                final_dict.update({word:splitted_text.count(word)})
            self.__text_counted = final_dict
        #
        if key_word == None:
            return self.__text_counted
        else:
            if key_word in self.__text_counted.keys():
                return self.__text_counted[key_word]
            else:
                return 0
    #        
    def lemmatize(self, language="it"):
        #
        global simplemma
        if "simplemma" not in globals():
            if self.verbose:
                print("I need a lemmatization library. I'm executing 'import simplemma'.")
            try:
                import simplemma
            except Exception as exc:
                print("Error while importing the simplemma library.\nI cannot lemmatize the words.")
                return dict({})
        global pd
        if "pd" not in globals():
            if self.verbose:
                print("I need pandas. I'm executing 'import pandas'.")
            try:
                import pandas as pd
            except Exception as exc:
                print("Error while importing the pandas library.\nI cannot lemmatize the words.")
                return dict({})
        #
        if self.__none_check(self.__text_counted):
            self.word_count()  
        #
        if self.__none_check(self.__text_lemmatized):
            if self.verbose:
                print("I am lemmatizing the text. Please wait.") 
            self.__text_lemmatized = dict(self.__text_counted)
            words_list = self.__text_lemmatized.keys()
            #
            repl_dict = replace_dict_func(language)
            if repl_dict != dict({}):
                for old_word in list(words_list):
                    new_word = repl_dict.get(old_word, old_word)
                    self.__text_lemmatized[new_word] = self.__text_lemmatized.pop(old_word)
            #
            words_list_lemmatized = []
            words_list_count = []
            for i,word in enumerate(words_list):
                words_list_lemmatized.append(simplemma.lemmatize(word, lang=language))
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
        if self.__none_check(self.__text_lemmatized):
            language = input("Please specify a language (for default press enter): ")
            if language == '':
                language = 'it'
            self.lemmatize(self, language)
        #
        if self.__none_check(self.__text_lemma_counted):
            if self.verbose:
                print("I am counting the lemmas. Please wait.")
            lemma_occurrences = self.__text_lemmatized.groupby("Lemma")["Raw"].unique().reset_index()
            lemma_occurrences.columns = ['Lemma', 'Occurrence']
            lemma_counts = self.__text_lemmatized.groupby("Lemma")["Raw Count"].sum().reset_index()
            lemma_counts.columns = ['Lemma', 'Lemma Count']
            self.__text_lemma_counted = lemma_counts.merge(lemma_occurrences, on = "Lemma")    
        #       
        return self.__text_lemma_counteds