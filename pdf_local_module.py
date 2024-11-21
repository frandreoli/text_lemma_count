#
class pdf_analyzer:
    #
    #Initialization
    def __init__ (self,path : str, verbose : bool = True):
        self._file_path = path
        self.verbose = verbose
        global pypdf
        if "pypdf" not in globals():
            if self.verbose:
                print("I need the pypdf library. I'm executing 'import pypdf'.")
            import pypdf
        global pd
        if "pd" not in globals():
            if self.verbose:
                print("I need the pandas library. I'm executing 'import pandas as pd'.")
            import pandas as pd
        self.__reader = pypdf.PdfReader(self._file_path)
        self._n_pages = len(self.__reader.pages)
        self.__extracted_text = pd.Series(["" for _ in range(0,self._n_pages)])
        self.__extracted_pages = set([])
    #
    #Retrieve the file path without allowing for changes
    @property
    def file_path(self):
        return self._file_path
    @file_path.setter
    def file_path(self, value):
        raise AttributeError("WARNING: The file path is read-only and cannot be modified.")
    @property
    def n_pages(self):
        return self._n_pages
    @n_pages.setter
    def n_pages(self, value):
        raise AttributeError("WARNING: The number of pages is read-only and cannot be modified.")
    #
    #Extracting the pages
    def extract(self,i_start = None,j_end = None,*,force : bool = False, merge: bool = False):
        if type(j_end)==type(None) and type(i_start)!=list:
            j_end = i_start
        if type(j_end)==int and j_end<0:
            j_end = self._n_pages+j_end+1
        if type(i_start)==list and type(j_end)!=type(None) and self.verbose:
            print("WARNING: The first argument already specifies a list of pages. I will ignore the second argument.")
        #
        error_i_type = "WARNING: When explicitly added, the first argument of the method 'extract' must be either an integer or a ist of integers."
        error_i_value = f"WARNING: The page indices must be contained between 1 and n_pages = {self._n_pages}"
        exit_return = []
        #
        if type(i_start)==type(None):
            page_list = range(0,self._n_pages)  
        #  
        elif type(i_start)==list:
            page_list = set(i_start)
            #Checking that the pages are correct
            for page in page_list:
                if type(page)!=int:
                    print(error_i_type)
                    return exit_return
                elif page<1 or page>self._n_pages:
                    print(error_i_value)
                    return exit_return
            page_list = [page - 1 for page in page_list]
        #        
        elif type(i_start)==int:
            if i_start<1 or i_start>self._n_pages:
                print(error_i_value)
                return exit_return
            if  type(j_end)!=int or j_end>self._n_pages or j_end<i_start:
                print(f"WARNING: The end of the page range must be an integer larger than the starting index {i_start} and smaller than {self._n_pages}")
                return exit_return
            if j_end == i_start:
                page_list = [i_start-1]
            else:
                page_list = range(i_start-1,j_end-1)
        #
        else:
            print(error_i_type)
            return exit_return
        #
        #Removing the pages already extracted from the list
        if not force:
            page_list = set(page_list) - self.__extracted_pages
        #
        page_list = sorted(list(page_list))
        #
        #Extracting the text
        for page in page_list:
            self.__extracted_text[page] = self.__reader.pages[page].extract_text()
            self.__extracted_pages.add(page)
        #
        if merge:
            return "\n\n".join(list(self.__extracted_text[page_list]))
        else:
            return list(self.__extracted_text[page_list])
    #
    