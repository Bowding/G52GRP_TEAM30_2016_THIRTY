import unittest
from bottle_index import get_target_url

def scholar_error_message(input): 
        return ("Error: Scholar '" + input + "' not found.\n\nTry to search using Google Scholar profile URL. e.g. https://scholar.google.co.uk/citations?user=...")

url_error_message = "Error: Invalid URL. Please enter valid Google Scholar profile URL. e.g. https://scholar.google.co.uk/citations?user=..."

class InputDefectTests(unittest.TestCase):   

    def test_URL(self):
        self.assertEqual(get_target_url("www..com"), url_error_message)         # blank URL
        self.assertEqual(get_target_url("google.co.uk"), url_error_message)     # invaild URL
        self.assertEqual(get_target_url("https://scholar.google.co.uk/citations?user=Fhufy87Fjhfjhej"), url_error_message) # broken scholar URL i.e. everything after 'user=' is random
        self.assertEqual(get_target_url("https://scholar.google.co.uk/citations?user=Fhufy87Fjhfjhej"), url_error_message) # broken scholar URL i.e. everything after 'user=' is random
        #self.assertEqual(get_target_url("google.fr"), url_error_message) # foreign URL (This won't work. Can't get error checking on all URLS. An error will be returned)
      
    def test_SCHOLAR(self):
        self.assertEqual(get_target_url(""), scholar_error_message(""))                 # blank Input
        self.assertEqual(get_target_url("hauiwdhc7iu"), scholar_error_message("hauiwdhc7iu"))      # garbage text
        self.assertEqual(get_target_url("Nicholas Victoros"), scholar_error_message("Nicholas Victoros"))# known name that is not on Google Scholar (my name)
        
class InputValidationTests(unittest.TestCase):   
    def test_URL(self):
        self.assertEqual(get_target_url("https://scholar.google.co.uk/citations?user=qc6CJjYAAAAJ&hl=en&oi=ao"), # Albert Einstein Link
                                        "https://scholar.google.co.uk/citations?user=qc6CJjYAAAAJ&hl=en&oi=ao")
										
if __name__ == "__main__":
    unittest.main()	