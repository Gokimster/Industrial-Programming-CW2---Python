#!/bin/env python
# 

import sys
import json
import getopt
import matplotlib.pyplot as plt
import operator


# -----------------------------------------------------------------------------
# Constants
jfile = 'issuu_cw2.json'

continents = {
  'AF' : 'Africa',
  'AS' : 'Asia',
  'EU' : 'Europe',
  'NA' : 'North America',
  'SA' : 'South America',
  'OC' : 'Oceania',
  'AN' : 'Antarctica'
}

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
def loadJSON():
    records = [ json.loads(line) for line in open(jfile) ]
    return records

def task2(records, doc):
    country_count = {}
    match_records = []
    for entry in records:
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
def task2a(records, doc):
    country_count = task2(records, doc)
    show_histo(country_count, "vert", "Views per Country", "Country Distribution")

def task2b(records, doc):
    country_count = task2(records, doc)
    cont_count = {}
    for cntry in country_count:
        if (cntry_to_cont[cntry] in cont_count):
            cont_count[cntry_to_cont[cntry]] += country_count[cntry]
        else:
            cont_count[cntry_to_cont[cntry]] = country_count[cntry]
    show_histo(cont_count, "vert", "Views per Continent", "Continent Distribution")

def show_histo(dict, orient="horiz", label="counts", title="title"):
    """Take a dictionary of counts and show it as a histogram."""
    if orient=="horiz":
        bar_fun = plt.barh     # NB: this assigns a function to bar_fun!
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
    bar_ticks(range(n), list(dict.keys()))  # NB: uses a higher-order function
    bar_label(label)
    plt.title(title)
    plt.show()

def task3a(records):
    browser_count = {}
    for entry in records:
        if(entry['visitor_device'] == 'browser'):
            if (entry['visitor_useragent'] in browser_count):
                browser_count[entry['visitor_useragent']] += 1
            else:
                browser_count[entry['visitor_useragent']] = 1
    show_histo(browser_count, "vert", "Number of Accesses using Browser", "Browser Distribution")

def task3b(records):
    browser_count = {}
    for entry in records:
        if(entry['visitor_device'] == 'browser'):
            if (entry['visitor_useragent'].find('/') > -1):
                browser = entry['visitor_useragent'][0:entry['visitor_useragent'].find('/')]
            else: browser = entry['visitor_useragent']
            if (browser in browser_count):
                browser_count[browser] += 1
            else:
                browser_count[browser] = 1
    show_histo(browser_count, "vert", "Number of Accesses using Browser", "Browser Distribution")

def task4(records):
    user_readTimes = {}
    for entry in records:
        if(entry['event_type'] == 'pagereadtime'):
            if (entry['visitor_uuid'] in user_readTimes):
                user_readTimes[entry['visitor_uuid']] += entry['event_readtime']
            else:
                user_readTimes[entry['visitor_uuid']] = entry['event_readtime']
    readTimes = sorted(user_readTimes.items(), key=operator.itemgetter(1), reverse = True)
    i = 0
    for times in readTimes:
        if(i > 9):
            break
        print(readTimes[i])
        i += 1


# main
if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "u:d:t:")
    except getopt.GetoptError as err:
        # print help information and exit:
        #print str(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    for o, a in opts:
        if o == "-u":
            user = a
        elif o == "-d":
            doc = a
        elif o == "-t":
            task = a
        else:
            assert False, "unhandled option"
    records = loadJSON()
    print(user, doc, task);
    if task == "2a":
        task2a(records, doc)
    elif task == "2b":
        task2b(records, doc)
    elif task == "3a":
        task3a(records)
    elif task =="3b":
        task3b(records)
    elif task == "4":
        task4(records)
        