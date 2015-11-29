import sys
import json
import getopt
import matplotlib.pyplot as plt
import operator
from tkinter import *
from tkinter import ttk


#--------------------------------------------
#Constants
#--------------------------------------------
jfile = 'issuu_cw2.json'

#--------------------------------------------
#Task Executer Class
#--------------------------------------------
class TaskExecuter:

    def __init__(self):
        self.records = self.loadJSON()

    def loadJSON(self) -> list:
        records = [ json.loads(line) for line in open(jfile) ]
        return records

    def executeTask(self, user, doc, task):
        """Takes a user uuid, doc uuid and a task and returns the output for the specific task"""
        if task == "2a":
            if(doc !=""):
                return self.task2a(doc)
            else:
                return "DOC UUID needs to be specified"
        elif task == "2b":
            if(doc !=""):
                return self.task2b(doc)
            else:
                return "DOC UUID needs to be specified"
        elif task == "3a":
            return self.task3a()
        elif task =="3b":
            return self.task3b()
        elif task == "4":
            return self.listToStringFormat(self.task4())
        elif task == "5a":
            return self.listToStringFormat(self.task5(doc, user, sorting ="readership"))
        elif task == "5b":
            return self.listToStringFormat(self.task5(doc, user, sorting = "count"))
        else:
            print("NO SUCH TASK")
            return "NO SUCH TASK"

    def listToStringFormat(self, list) ->str:
        """Takes a list and returns a string representation of that list"""
        string = ''
        for element in list:
            string = string + str(element) + "\n"
        return string

    def task2(self, doc) -> dict:
        """"Take a document UUID and return a  dictionary in which the keys are the countries in which the document
        has been read in and the values are the number of times the document has been read from that country """
        country_count = {}
        match_records = []
        for entry in self.records:
            if (entry['event_type'] =='read'):
                if entry['subject_doc_id'] == doc:
                    match_records.append(entry)
        for rec in match_records:
            if (rec['visitor_country'] in country_count):
                country_count[rec['visitor_country']] += 1
            else:
                country_count[rec['visitor_country']] = 1
        print(country_count)
        return country_count

    def task2a(self, doc):
        """"Take a document UUID and show a histogram of the countries that the document has been read in and 
        the number of times that it has been read for each country"""
        country_count = self.task2(doc)
        self.show_histo(country_count, "vert", "Reads per Country", "Country Distribution")

    def task2b(self, doc):
        """"Take a document UUID and show a histogram of the continents that the document has been read in and 
        the number of times that it has been read for each continent"""
        country_count = self.task2(doc)
        cont_count = {}
        for cntry in country_count:
            if (cntry_to_cont[cntry] in cont_count):
                cont_count[cntry_to_cont[cntry]] += country_count[cntry]
            else:
                cont_count[cntry_to_cont[cntry]] = country_count[cntry]
        self.show_histo(cont_count, "vert", "Views per Continent", "Continent Distribution")

    def show_histo(self, dict, orient="horiz", label="counts", title="title"):
        """Take a dictionary of counts and show it as a histogram."""
        if orient=="horiz":
            bar_fun = plt.barh 
            bar_ticks = plt.yticks
            bar_label = plt.xlabel
        elif orient=="vert":
            bar_fun = plt.bar
            bar_ticks = plt.xticks
            bar_label = plt.ylabel
        else:
            raise Exception("show_histo: Unknown orientation: %s ".format % orient)
        n = len(dict)
        bar_fun(range(n), list(dict.values()), align='center', alpha=0.4)
        bar_ticks(range(n), list(dict.keys())) 
        bar_label(label)
        plt.title(title)
        plt.show()

    def task3a(self):
        """Show a histogram of the browsers used by viewers"""
        browser_count = {}
        for entry in self.records:
            if((entry['visitor_device'] == 'browser')  and (entry['event_type'] == 'read')):
                browser = entry['visitor_useragent']
                if (browser in browser_count):
                    browser_count[entry['visitor_useragent']] += 1
                else:
                    browser_count[entry['visitor_useragent']] = 1
        self.show_histo(browser_count, "vert", "Number of Accesses using Browser", "Browser Distribution")

    def task3b(self):
        """Show a histogram of the browsers used by viewers - just the browser name"""
        browser_count = {}
        for entry in self.records:
            if((entry['visitor_device'] == 'browser') and (entry['event_type'] == 'read')):
                if (entry['visitor_useragent'].find('/') > -1):
                    browser = entry['visitor_useragent'][0:entry['visitor_useragent'].find('/')]
                else: browser = entry['visitor_useragent']
                if (browser in browser_count):
                    browser_count[browser] += 1
                else:
                    browser_count[browser] = 1
        self.show_histo(browser_count, "vert", "Number of Accesses using Browser", "Browser Distribution")

    def task4(self) ->list:
        """Return the top 10 readers in the records"""
        user_readTimes = {}
        for entry in self.records:
            if(entry['event_type'] == 'pagereadtime'):
                if (entry['visitor_uuid'] in user_readTimes):
                    user_readTimes[entry['visitor_uuid']] += entry['event_readtime']
                else:
                    user_readTimes[entry['visitor_uuid']] = entry['event_readtime']
        readTimes = list(sorted(user_readTimes.items(), key=operator.itemgetter(1), reverse = True))[0:10]
        for times in readTimes:
            print(times)
        return readTimes

    def task5(self, doc_uuid, visitor_uuid, sorting = "count")-> list:
        """Takes a document uuid, visitor uuid and a type of sorting and returns a list of "also-liked" documents sorted
        differently depending on the type"""
        tmp = []
        if (sorting == "readership"):
            tmp = self.alsoLike(doc_uuid, visitor_uuid, self.sortByReadership)
        elif (sorting == "count"):
            tmp = self.alsoLike(doc_uuid, visitor_uuid, self.sortByReadCount)
        else:
            tmp = ["No Such Task"]
        print(self.listToStringFormat(tmp))
        return tmp

    def getDocVisitors(self, doc_uuid) -> list:
        """Takes a document UUID and returns a list of all the visitor UUIDs that read that document"""
        user_uuids = []
        for entry in self.records:
            if((entry['event_type'] =='read') and (entry['subject_doc_id'] == doc_uuid) and (not(entry['visitor_uuid'] in user_uuids))):
                user_uuids.append(entry['visitor_uuid'])
        return user_uuids

    def getDocsForVisitor(self, visitor_uuid) -> list:
        """Takes a visitor UUID and returns a ist of all the documents read by that visitor"""
        doc_uuids = []
        for entry in self.records:
            if ((entry['event_type'] =='read') and (entry['visitor_uuid'] == visitor_uuid)):
                doc_uuids.append(entry['subject_doc_id'])
        return doc_uuids

    def alsoLike(self, doc_uuid, visitor_uuid, sort_fun) -> list:
        """Takes a document uuid, visitor uuid and a sorting function and returns a list of "also-liked" documents sorted
        by the given function"""
        user_uuids = self.getDocVisitors(doc_uuid)
        try:
            user_uuids.remove(visitor_uuid)
        except:
            pass
        return sort_fun(user_uuids, doc_uuid)[0:10]

    def sortByReadCount(self, user_uuids, doc_uuid) -> list:
        """Takes a ist of user UUIDs and a doc UUID and returns a list of all the docs read by those viewers sorted 
        by how many users in the list read them"""
        docs = {}
        for user_uuid in user_uuids:
            visitor_docs = self.getDocsForVisitor(user_uuid)
            for doc in visitor_docs:
                if(doc != doc_uuid):
                    if (doc in docs):
                        docs[doc] += 1
                    else: 
                        docs[doc] = 1
        return list(sorted(docs.items(), key=operator.itemgetter(1), reverse = True))

    def sortByReadership(self, user_uuids, doc_uuid) -> list:
        """Takes a ist of user UUIDs and a doc UUID and returns a list of all the docs read by those viewers sorted 
        by how many users in the list read them"""
        docs = {}
        for entry in self.records:
            if ((entry['event_type'] =='pagereadtime') and (entry['visitor_uuid'] in user_uuids)):
                doc = entry['subject_doc_id']
                if(doc != doc_uuid):
                    if(doc in docs):
                        docs[doc] += int(entry['event_readtime'])
                    else:
                        docs[doc] = int(entry['event_readtime'])
        return list(sorted(docs.items(), key = operator.itemgetter(1), reverse = True))
        
#--------------------------------------------
#GUI Class
#--------------------------------------------
class GUI:

    def __init__(self):
        """initialisation of the UI"""
        self.root = Tk()
        self.root.title("Coursework 2")

        mainframe = ttk.Frame(self.root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)

        self.visitor_uuid = StringVar()
        self.document_uuid = StringVar()
        self.task = StringVar()

        visitor_entry = ttk.Entry(mainframe, width=30, textvariable=self.visitor_uuid)
        visitor_entry.grid(column=2, row=1, sticky=(W, E))

        document_entry = ttk.Entry(mainframe, width=30, textvariable=self.document_uuid)
        document_entry.grid(column=2, row=2, sticky=(W, E))

        task_entry = ttk.Entry(mainframe, width=2, textvariable=self.task)
        task_entry.grid(column=2, row=3, sticky=(W, E))

        ttk.Button(mainframe, text="Do Task", command=self.doTask).grid(column=2, row=4, sticky=W)

        ttk.Label(mainframe, text="Visitor UUID").grid(column=1, row=1, sticky=W)
        ttk.Label(mainframe, text="Document UUID").grid(column=1, row=2, sticky=E)
        ttk.Label(mainframe, text="Task").grid(column=1, row=3, sticky=W)
        
        self.output = StringVar()
        self.w = ttk.Label( mainframe, textvariable = self.output)
        self.w.grid(column = 1, row = 5, sticky=S)

        for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

        visitor_entry.focus()
        self.root.bind('<Return>', self.doTask)

        self.taskEx = TaskExecuter()
        self.root.mainloop()

    def doTask(self, *args):
        """Does the the task specified by the user and shows the output"""
        taskId = self.task.get()
        document = self.document_uuid.get()
        visitor = self.visitor_uuid.get()
        self.output.set(str(self.taskEx.executeTask(visitor, document, taskId)))




#--------------------------------------------
#Main Method
#--------------------------------------------
if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "u:d:t:")
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(0)
    user = ""
    doc = ""
    task = ""
    for o, a in opts:
        if o == "-u":
            user = a
        elif o == "-d":
            doc = a
        elif o == "-t":
            task = a
        else:
            assert False, "unhandled option"
    if((user == "") and (doc == "") and ( task == "")):
        gui = GUI()
    else:
        taskEx = TaskExecuter()
        taskEx.executeTask(user, doc, task)

#--------------------------------------------
#Dict Constants
#--------------------------------------------
cntry_to_cont = {
  'AF' : 'AS',
  'AX' : 'EU',
  'AL' : 'EU',
  'DZ' : 'AF',
  'AS' : 'OC',
  'AD' : 'EU',
  'AO' : 'AF',
  'AI' : 'NA',
  'AQ' : 'AN',
  'AG' : 'NA',
  'AR' : 'SA',
  'AM' : 'AS',
  'AW' : 'NA',
  'AU' : 'OC',
  'AT' : 'EU',
  'AZ' : 'AS',
  'BS' : 'NA',
  'BH' : 'AS',
  'BD' : 'AS',
  'BB' : 'NA',
  'BY' : 'EU',
  'BE' : 'EU',
  'BZ' : 'NA',
  'BJ' : 'AF',
  'BM' : 'NA',
  'BT' : 'AS',
  'BO' : 'SA',
  'BQ' : 'NA',
  'BA' : 'EU',
  'BW' : 'AF',
  'BV' : 'AN',
  'BR' : 'SA',
  'IO' : 'AS',
  'VG' : 'NA',
  'BN' : 'AS',
  'BG' : 'EU',
  'BF' : 'AF',
  'BI' : 'AF',
  'KH' : 'AS',
  'CM' : 'AF',
  'CA' : 'NA',
  'CV' : 'AF',
  'KY' : 'NA',
  'CF' : 'AF',
  'TD' : 'AF',
  'CL' : 'SA',
  'CN' : 'AS',
  'CX' : 'AS',
  'CC' : 'AS',
  'CO' : 'SA',
  'KM' : 'AF',
  'CD' : 'AF',
  'CG' : 'AF',
  'CK' : 'OC',
  'CR' : 'NA',
  'CI' : 'AF',
  'HR' : 'EU',
  'CU' : 'NA',
  'CW' : 'NA',
  'CY' : 'AS',
  'CZ' : 'EU',
  'DK' : 'EU',
  'DJ' : 'AF',
  'DM' : 'NA',
  'DO' : 'NA',
  'EC' : 'SA',
  'EG' : 'AF',
  'SV' : 'NA',
  'GQ' : 'AF',
  'ER' : 'AF',
  'EE' : 'EU',
  'ET' : 'AF',
  'FO' : 'EU',
  'FK' : 'SA',
  'FJ' : 'OC',
  'FI' : 'EU',
  'FR' : 'EU',
  'GF' : 'SA',
  'PF' : 'OC',
  'TF' : 'AN',
  'GA' : 'AF',
  'GM' : 'AF',
  'GE' : 'AS',
  'DE' : 'EU',
  'GH' : 'AF',
  'GI' : 'EU',
  'GR' : 'EU',
  'GL' : 'NA',
  'GD' : 'NA',
  'GP' : 'NA',
  'GU' : 'OC',
  'GT' : 'NA',
  'GG' : 'EU',
  'GN' : 'AF',
  'GW' : 'AF',
  'GY' : 'SA',
  'HT' : 'NA',
  'HM' : 'AN',
  'VA' : 'EU',
  'HN' : 'NA',
  'HK' : 'AS',
  'HU' : 'EU',
  'IS' : 'EU',
  'IN' : 'AS',
  'ID' : 'AS',
  'IR' : 'AS',
  'IQ' : 'AS',
  'IE' : 'EU',
  'IM' : 'EU',
  'IL' : 'AS',
  'IT' : 'EU',
  'JM' : 'NA',
  'JP' : 'AS',
  'JE' : 'EU',
  'JO' : 'AS',
  'KZ' : 'AS',
  'KE' : 'AF',
  'KI' : 'OC',
  'KP' : 'AS',
  'KR' : 'AS',
  'KW' : 'AS',
  'KG' : 'AS',
  'LA' : 'AS',
  'LV' : 'EU',
  'LB' : 'AS',
  'LS' : 'AF',
  'LR' : 'AF',
  'LY' : 'AF',
  'LI' : 'EU',
  'LT' : 'EU',
  'LU' : 'EU',
  'MO' : 'AS',
  'MK' : 'EU',
  'MG' : 'AF',
  'MW' : 'AF',
  'MY' : 'AS',
  'MV' : 'AS',
  'ML' : 'AF',
  'MT' : 'EU',
  'MH' : 'OC',
  'MQ' : 'NA',
  'MR' : 'AF',
  'MU' : 'AF',
  'YT' : 'AF',
  'MX' : 'NA',
  'FM' : 'OC',
  'MD' : 'EU',
  'MC' : 'EU',
  'MN' : 'AS',
  'ME' : 'EU',
  'MS' : 'NA',
  'MA' : 'AF',
  'MZ' : 'AF',
  'MM' : 'AS',
  'NA' : 'AF',
  'NR' : 'OC',
  'NP' : 'AS',
  'NL' : 'EU',
  'NC' : 'OC',
  'NZ' : 'OC',
  'NI' : 'NA',
  'NE' : 'AF',
  'NG' : 'AF',
  'NU' : 'OC',
  'NF' : 'OC',
  'MP' : 'OC',
  'NO' : 'EU',
  'OM' : 'AS',
  'PK' : 'AS',
  'PW' : 'OC',
  'PS' : 'AS',
  'PA' : 'NA',
  'PG' : 'OC',
  'PY' : 'SA',
  'PE' : 'SA',
  'PH' : 'AS',
  'PN' : 'OC',
  'PL' : 'EU',
  'PT' : 'EU',
  'PR' : 'NA',
  'QA' : 'AS',
  'RE' : 'AF',
  'RO' : 'EU',
  'RU' : 'EU',
  'RW' : 'AF',
  'BL' : 'NA',
  'SH' : 'AF',
  'KN' : 'NA',
  'LC' : 'NA',
  'MF' : 'NA',
  'PM' : 'NA',
  'VC' : 'NA',
  'WS' : 'OC',
  'SM' : 'EU',
  'ST' : 'AF',
  'SA' : 'AS',
  'SN' : 'AF',
  'RS' : 'EU',
  'SC' : 'AF',
  'SL' : 'AF',
  'SG' : 'AS',
  'SX' : 'NA',
  'SK' : 'EU',
  'SI' : 'EU',
  'SB' : 'OC',
  'SO' : 'AF',
  'ZA' : 'AF',
  'GS' : 'AN',
  'SS' : 'AF',
  'ES' : 'EU',
  'LK' : 'AS',
  'SD' : 'AF',
  'SR' : 'SA',
  'SJ' : 'EU',
  'SZ' : 'AF',
  'SE' : 'EU',
  'CH' : 'EU',
  'SY' : 'AS',
  'TW' : 'AS',
  'TJ' : 'AS',
  'TZ' : 'AF',
  'TH' : 'AS',
  'TL' : 'AS',
  'TG' : 'AF',
  'TK' : 'OC',
  'TO' : 'OC',
  'TT' : 'NA',
  'TN' : 'AF',
  'TR' : 'AS',
  'TM' : 'AS',
  'TC' : 'NA',
  'TV' : 'OC',
  'UG' : 'AF',
  'UA' : 'EU',
  'AE' : 'AS',
  'GB' : 'EU',
  'US' : 'NA',
  'UM' : 'OC',
  'VI' : 'NA',
  'UY' : 'SA',
  'UZ' : 'AS',
  'UK' : 'EU',
  'VU' : 'OC',
  'VE' : 'SA',
  'VN' : 'AS',
  'WF' : 'OC',
  'EH' : 'AF',
  'YE' : 'AS',
  'ZM' : 'AF',
  'ZW' : 'AF'
}
        