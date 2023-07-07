import requests
import sys
import time

units = {	
'B' : {'size':1, 'speed':'B/s'},
'KB' : {'size':1024, 'speed':'KB/s'},
'MB' : {'size':1048576, 'speed':'MB/s'},
'GB' : {'size':1073741824, 'speed':'GB/s'},
'TB' : {'size':1099511627776, 'speed':'TB/s'},
'PB' : {'size':1125899906842624, 'speed':'PB/s'}
}

time_list = {
's' : {'unit':1},
'm' : {'unit':60},
'h' : {'unit':3600},
'd' : {'unit':86400}
}

#time in units
def check_time(eta):
    if eta >= 0 and eta < 60:
        return 's'
    elif eta >= 60 and eta < 3600:
        return 'm'
    elif eta >= 3600 and eta < 86400:
        return 'h'
    elif eta >= 86400:
        return 'd'

# length in units
def check_unit(length):
    if length > 0 and length < 1024:
        return 'B'
    elif length >= 1024 and length < 1048576:
        return 'KB'
    elif length >= 1048576 and length < 1073741824:
        return 'MB'
    elif length >= 1073741824 and length < 1099511627776:
        return 'GB'
    elif length >= 1099511627776 and length < 1125899906842624:
        return 'TB'
    elif length >= 1125899906842624:
        return 'PB'

# link and saved directory
def downloadFile(url, directory) :

    # file name
    localFilename = url.split('/')[-1]

    with open(directory + '/' + localFilename, 'wb') as f:
        print ("Downloading . . .\n")

        # start time
        start = time.time()
        r = requests.get(url, stream=True)

        # total length in bytes of the file
        total_length = float(r.headers.get('content-length'))

        # download value
        d = 0

        i = 0
        
        # Availability
        if total_length is not None:

            # file: total_length in proper unit
            file_unit = check_unit(total_length)
            tl = total_length / units[file_unit]['size']

            for chunk in r.iter_content(8192):
                d += float(len(chunk))

                # file: writing the file in chunks of 8192 bytes
                f.write(chunk)

                # file: downloaded percentage
                done = 100 * d / total_length

                # file: downloaded in proper unit
                downloaded = d / units[check_unit(d)]['size']

                # speed: speed in bytes per sec
                trs = d // (time.time() - start)

                # speed: speed in proper unit
                download_speed = trs / units[check_unit(trs)]['size']

                # speed: speed unit
                speed_unit = units[check_unit(trs)]['speed']

                # AVG speed: average speed
                if i == 0:
                    average_speed = trs

                average_speed = 0.005 * trs + 0.995 * average_speed

                # ETA: estimated time arrival
                eta = (total_length - d) // average_speed

                # ETA: estimated time arrival unit
                eta_unit = check_time(eta)

                # ETA: estimated time arrival in proper unit
                eta_final = eta / time_list[check_time(eta)]['unit']
                
                fmt_string = "\r%.5f%s [%s%s] %.5f %s / %.5f %s  SPEED:%.5f %s  ETA:%i %s     "
                set_of_vars = (done, '%',
                                '*' * (int(done)//10),
                                '_' * (10-int(done)//10),
                                downloaded, check_unit(d),
                                tl, file_unit,
                                download_speed, speed_unit, eta_final, eta_unit)

                sys.stdout.write(fmt_string % set_of_vars)
                sys.stdout.flush()
        else:
            f.write(r.content)

    # total time taken for download
    return (time.time() - start)

def main() :
    directory = '.'
    if len(sys.argv) > 1 :

        # url from cmd line arg
        url = sys.argv[1]
        if len(sys.argv) > 2:
            directory = sys.argv[2]

            total_time = downloadFile(url, directory)
            print ("\r\nDownload complete...\r\nTime Elapsed: %f s" % total_time)

        else :
            print("Something went wrong and can't figure out why (not that i have any troubleshooting mechanism)")

if __name__ == "__main__" :
    main()
