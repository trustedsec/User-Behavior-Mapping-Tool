#!/usr/bin/env python3
# Script that parses the sqlite3 database ActivityCache.db that comes from Windows Timeline and outputs reports and charts
# Author: Oddvar Moe - TrustedSec
# Version: 1.2
# Based on https://github.com/kacos2000/WindowsTimeline/blob/master/WinTimelineOffline.ps1
import argparse
import sqlite3
import json
import pandas as pd
import base64
import re
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict
import csv
import os
import sys
from termcolor import colored

if __name__ == '__main__':
    logo = '''
                                =vxr^rui))^^^<                                   
                        .=(()*^(v!'         _LIu}ir;_`                           
                    `?x|r:`'____`             :~ri}Tv}yVuvr?iyv~_                
                 `;v)!  `__-  .___:^:-        -__.,<r\<_._____!~(ixr.            
                vMx'  -_-   ._.'___.____-`_`__` :v**~;"!_` -_______vM^           
               )v` `__`   `,!__-  __  .__Y!>)` `_ :Vx*!:",<='`!-   `.GG~         
             `y! `__.,  _^;_'   `:"__,=:*)_T=.   ~<>*!,<!-:<!,"x!_=! `<Ux        
            ;X_  ` '~",!:!` ,~_<L]L^~xLir:v("_. `_!~*ur=*<>:^=!\<~:vr' `Tv`      
          'PV`   .<=-  `!` _()v*!!Lo}x*?iv;v).=_ ._.:=vVzc^!:^r<<=*~*)*_`xh).    
        ,rx_ -___",__=,,,__:(*))*yVx*<::^ir_  ^ ._!^:}v, .:_"_">^<~:*~>*=:Mgl    
      :M6*__~!==_:!<<.`:;^^=`  `:-.=r^^~_`.,  *`   ';=rv:="~,*Y^~<~<^~_>*!:I"    
     !di` ____!___`;r_:: <_-:::<_"=_.  ~. ~~ 'u` `__,^rv:.!,=)~vvrL~x(~:_=*xb,   
     !T  ", !```."rT=-*v_u~.,>=,_ ``   ~~ x* **    `:;:-)::)::x-.=i]._::^<~^)j-  
     l; `~ !_.)^-.\="(\).v-_`  _"    `_(-.w":)  _=   `:_:^``~!!L= ,r<,-:'_!:,)y  
     c- =.'!_,r!^=:;.*Tu\!`   __`_=!~^!,,}|!`~   ~     ``:)` i- r: ',=~=-:~:'}V  
    `X` ~ :__^=` -Lr*mwk-`,_:~=x*=' `!*~!>_`," '.~ `   ~ -: .*~ '):`.v~~``r* TP  
    rZ ``=!,)v^^|x?Yv*,^)``!`_-~_x<^|z:~=__.-_`-.~"`   ~`` '^"`  ~ ! -*<<:^;! y` 
    II  `}!~'-rxr~:_-__,`  ~  !(.)- :r     `. :?_.=`  `=  `_     _ `! :);'i"~^T  
   `z;  r!=`,`:^<:___`   ` ~_!^^_- `v'  -~)^:_)=:~=:___`           ', `-r!,!=e:  
   u*  ^} ^-`='^^^:_____:)vxr~_`___>= .:"<^::!~__-__`   '=ri**^^^*r)iT=` -:!`y~  
   Z~ -xr-,~=-: -::______`._-_:<!::<=~~,::-`           -m}`.        .iu   :_ =c  
  `g=,_=)!=` _::` -___,!!><:!__'                   `(T*r!           ^y*   `.`rV  
  _6x- !!_^v'._:__`  `___-'   ':=,<*^^r?L*!--=~``^VI\`       `-!^(xLxuGT~,=-cw`  
   ~6` ~ _,^":~":.__`     -\3y^=!<*rr^!,-_:)*:^Px:     ")ivvxL}Lxvv}g#@@@d*'su   
   .5` ~   '~ `"_:*aBs,,}xxcYxcXH5H3PGaKHMdZV!.`   ,iPKx_  '!^*^`   c~w@y^!*)w   
   `Y? `:'  -!     ,G#@Q}I8@#0jv!.        -=V##QQQB@@y `=**ZD3]V,   ^YIzo._=xK_  
     rv_ ._- `__-   T*^P#@@@Y `*xTkms35ZPi`  i@gr"~G@=.xVr^)**.      x6^z|I}_    
      '**r~`    .-  V"  -l##- ;=_____--.'-- `W@^    )y.<xx^<,-`     \#P*my:      
          ~}^"!vZ_  c!    (@*   .____:^^=_ `e#x      -oT!-____""<LMOGM-uM_       
           `ww!`T=  :V`    lO.    `-__-` '^6Q*         rmkcws5ZMh}<`_OD*         
             xT^")x. :u.    !whyIzVVkUHdROmY^`       `'=`.          :O~          
              y-;^iX  _V`     _riivvv\*!~.-c:v^      `VK?y`         *}           
              V.  :u   L*              !l vv  y.      xyV=l`        T=           
              Y'_:.rxx<xc             ;T` `vr~X"      um~ !L!       a*`          
             .L -*_`vQ~=_          -r(~      "^r*^^^^^*`    ~*~` _` V       
             v=: ,!*=g!       .` :}*.                            c!~~     
             ),,x-'P*ex       u= i`                    ` `:;     y!W-       
              V-|i]0k_V_      ri     .ryevuM3TVY*^))*XkZU}GV.  `x*vd_           
              -uqirgY -u:  ~: 'y`   `*.*hi,u* )M__W: *vy^~}    c,*])_            
               `xiV'   `wy`'_  ~}`      )<*yv^ua^^mr^v*'rv`   _x*Y )_    OH BEHAVE!!        
               _rk'    'kWx!    .r`      <\^-     `!)^rr.     `L^  x-            
            :ix^o~     L^V'<v<`            _^^^^^r)*!'       :T:   uT-           
        "*vWm= _V     `V ]v  :()"                          :T*`    V'L^          
   ->***)Lv,   x?     _V 'Z_   `<)):                     ^xGx     :V  *i'        
***^, `(v-     V,     `V  Li)~`   `~r**_              !rr~=u      T~   _Y~       
     ^i_       V       V, `u`:rr^-    .<**^^~:,__:~**r!` _V'     _V      ^],     
   'Y<        !3       (v  _\r=`-^**^:`    <e~~^>)}?^^^.=T'      c:       `)T~   
    '''
    parser = argparse.ArgumentParser(description='Tool for parsing ActivityCache.db and generating reports and charts. Will output files (csv and jpg) in the current directory.')
    parser.add_argument('-f','--file', default=None, type=str, help='Path to ActivityCache.db')
    parser.add_argument('-o','--outfolder', default=os.getcwd(), type=str, help='Output folder - Default is scripts working directory - Ex: /root/folder/test/')
    parser.add_argument('-m','--onlyexportmaindata', action='store_true', default=False, help='Set this to only export the main report and skip additional reports and charts generating')
    parser.add_argument('-v','--verbose', action='store_true', default=False, help='Enable Verbose Logging - Not implemented yet')

    args = parser.parse_args()
    if len(sys.argv)==1:
        print(colored("No arguments provided - Showing help\n", "red"))
        print(logo)
        parser.print_help()
        sys.exit(0)
        
    print(logo)
    file = args.file
    only_gen_main = args.onlyexportmaindata
    verbose = args.verbose
    outfolder = args.outfolder
    
    # Create outfolder if it does not exist
    isExist = os.path.exists(outfolder)
    if not isExist:
        os.makedirs(outfolder)
        

    # Connect to database and get data
    con = sqlite3.connect(file)
    con.text_factory = lambda b: b.decode(errors = 'ignore')
    cur = con.cursor()
    
    # Using Pandas to store the query
    query = cur.execute('''select 
       ETag,
       AppId, 
	   case when AppActivityId not like '%-%-%-%-%' then AppActivityId
		else trim(AppActivityId,'ECB32AF3-1440-4086-94E3-5311F97F89C4\') end as 'AppActivityId',
       ActivityType as 'Activity_type', 
       case ActivityStatus 
		when 1 then 'Active' when 2 then 'Updated' when 3 then 'Deleted' when 4 then 'Ignored' 
		end as 'ActivityStatus',
	   Smartlookup.'group' as 'Group', 
       MatchID,
       'No' AS 'IsInUploadQueue', 
	   Priority as 'Priority',	
	   ClipboardPayload,
       datetime(LastModifiedTime, 'unixepoch', 'localtime')as 'LastModifiedTime',
       datetime(ExpirationTime, 'unixepoch', 'localtime') as 'ExpirationTime',
       datetime(StartTime, 'unixepoch', 'localtime') as 'StartTime',
       datetime(EndTime, 'unixepoch', 'localtime') as 'EndTime',
	   case 
		when CreatedInCloud > 0 
		then datetime(CreatedInCloud, 'unixepoch', 'localtime') 
		else '' 
	   end as 'CreatedInCloud',
	   case 
		when OriginalLastModifiedOnClient > 0 
		then datetime(OriginalLastModifiedOnClient, 'unixepoch', 'localtime') 
		else '' 
	   end as 'OriginalLastModifiedOnClient',
       Tag,
       PlatformDeviceId,
       Payload from Smartlookup
       order by Etag desc''')
    
    dbdata = query.fetchall()

    known = {'308046B0AF4A39CB': 'Mozilla Firefox 64bit',
            'E7CF176E110C211B': 'Mozilla Firefox 32bit',
            'DE61D971-5EBC-4F02-A3A9-6C82895E5C04': 'AddNewPrograms',
            '724EF170-A42D-4FEF-9F26-B60E846FBA4F': 'AdminTools',
            'A520A1A4-1780-4FF6-BD18-167343C5AF16': 'AppDataLow',
            'A305CE99-F527-492B-8B1A-7E76FA98D6E4': 'AppUpdates',
            '9E52AB10-F80D-49DF-ACB8-4330F5687855': 'CDBurning',
            'DF7266AC-9274-4867-8D55-3BD661DE872D': 'ChangeRemovePrograms',
            'D0384E7D-BAC3-4797-8F14-CBA229B392B5': 'CommonAdminTools',
            'C1BAE2D0-10DF-4334-BEDD-7AA20B227A9D': 'CommonOEMLinks',
            '0139D44E-6AFE-49F2-8690-3DAFCAE6FFB8': 'CommonPrograms',
            'A4115719-D62E-491D-AA7C-E74B8BE3B067': 'CommonStartMenu',
            '82A5EA35-D9CD-47C5-9629-E15D2F714E6E': 'CommonStartup',
            'B94237E7-57AC-4347-9151-B08C6C32D1F7': 'CommonTemplates',
            '0AC0837C-BBF8-452A-850D-79D08E667CA7': 'Computer',
            '4BFEFB45-347D-4006-A5BE-AC0CB0567192': 'Conflict',
            '6F0CD92B-2E97-45D1-88FF-B0D186B8DEDD': 'Connections',
            '56784854-C6CB-462B-8169-88E350ACB882': 'Contacts',
            '82A74AEB-AEB4-465C-A014-D097EE346D63': 'ControlPanel',
            '2B0F765D-C0E9-4171-908E-08A611B84FF6': 'Cookies',
            'B4BFCC3A-DB2C-424C-B029-7FE99A87C641': 'Desktop',
            'FDD39AD0-238F-46AF-ADB4-6C85480369C7': 'Documents',
            '374DE290-123F-4565-9164-39C4925E467B': 'Downloads',
            '1777F761-68AD-4D8A-87BD-30B759FA33DD': 'Favorites',
            'FD228CB7-AE11-4AE3-864C-16F3910AB8FE': 'Fonts',
            'CAC52C1A-B53D-4EDC-92D7-6B2E8AC19434': 'Games',
            '054FAE61-4DD8-4787-80B6-090220C4B700': 'GameTasks',
            'D9DC8A3B-B784-432E-A781-5A1130A75963': 'History',
            '4D9F7874-4E0C-4904-967B-40B0D20C3E4B': 'Internet',
            '352481E8-33BE-4251-BA85-6007CAEDCF9D': 'InternetCache',
            'BFB9D5E0-C6A9-404C-B2B2-AE6DB6AF4968': 'Links',
            'F1B32785-6FBA-4FCF-9D55-7B8E7F157091': 'LocalAppData',
            '2A00375E-224C-49DE-B8D1-440DF7EF3DDC': 'LocalizedResourcesDir',
            '4BD8D571-6D19-48D3-BE97-422220080E43': 'Music',
            'C5ABBF53-E17F-4121-8900-86626FC2C973': 'NetHood',
            'D20BEEC4-5CA8-4905-AE3B-BF251EA09B53': 'Network',
            '2C36C0AA-5812-4B87-BFD0-4CD0DFB19B39': 'OriginalImages',
            '69D2CF90-FC33-4FB7-9A0C-EBB0F0FCB43C': 'PhotoAlbums',
            '33E28130-4E1E-4676-835A-98395C3BC3BB': 'Pictures',
            'DE92C1C7-837F-4F69-A3BB-86E631204A23': 'Playlists',
            '76FC4E2D-D6AD-4519-A663-37BD56068185': 'Printers',
            '9274BD8D-CFD1-41C3-B35E-B13F55A758F4': 'PrintHood',
            '5E6C858F-0E22-4760-9AFE-EA3317B67173': 'Profile',
            '62AB5D82-FDC1-4DC3-A9DD-070D1D495D97': 'ProgramData',
            '905E63B6-C1BF-494E-B29C-65B732D3D21A': 'ProgramFiles',
            'F7F1ED05-9F6D-47A2-AAAE-29D317C6F066': 'ProgramFilesCommon',
            '6365D5A7-0F0D-45E5-87F6-0DA56B6A4F7D': 'ProgramFilesCommonX64',
            'DE974D24-D9C6-4D3E-BF91-F4455120B917': 'ProgramFilesCommonX86',
            '6D809377-6AF0-444B-8957-A3773F02200E': 'ProgramFilesX64',
            '7C5A40EF-A0FB-4BFC-874A-C0F2E0B9FA8E': 'ProgramFilesX86',
            'A77F5D77-2E2B-44C3-A6A2-ABA601054A51': 'Programs',
            'DFDF76A2-C82A-4D63-906A-5644AC457385': 'Public',
            'C4AA340D-F20F-4863-AFEF-F87EF2E6BA25': 'PublicDesktop',
            'ED4824AF-DCE4-45A8-81E2-FC7965083634': 'PublicDocuments',
            '3D644C9B-1FB8-4F30-9B45-F670235F79C0': 'PublicDownloads',
            'DEBF2536-E1A8-4C59-B6A2-414586476AEA': 'PublicGameTasks',
            '3214FAB5-9757-4298-BB61-92A9DEAA44FF': 'PublicMusic',
            'B6EBFB86-6907-413C-9AF7-4FC2ABF07CC5': 'PublicPictures',
            '2400183A-6185-49FB-A2D8-4A392A602BA3': 'PublicVideos',
            '52A4F021-7B75-48A9-9F6B-4B87A210BC8F': 'QuickLaunch',
            'AE50C081-EBD2-438A-8655-8A092E34987A': 'Recent',
            'BD85E001-112E-431E-983B-7B15AC09FFF1': 'RecordedTV',
            'B7534046-3ECB-4C18-BE4E-64CD4CB7D6AC': 'RecycleBin',
            '8AD10C31-2ADB-4296-A8F7-E4701232C972': 'ResourceDir',
            '3EB685DB-65F9-4CF6-A03A-E3EF65729F3D': 'RoamingAppData',
            'B250C668-F57D-4EE1-A63C-290EE7D1AA1F': 'SampleMusic',
            'C4900540-2379-4C75-844B-64E6FAF8716B': 'SamplePictures',
            '15CA69B3-30EE-49C1-ACE1-6B5EC372AFB5': 'SamplePlaylists',
            '859EAD94-2E85-48AD-A71A-0969CB56A6CD': 'SampleVideos',
            '4C5C32FF-BB9D-43B0-B5B4-2D72E54EAAA4': 'SavedGames',
            '7D1D3A04-DEBB-4115-95CF-2F29DA2920DA': 'SavedSearches',
            'EE32E446-31CA-4ABA-814F-A5EBD2FD6D5E': 'SEARCH_CSC',
            '98EC0E18-2098-4D44-8644-66979315A281': 'SEARCH_MAPI',
            '190337D1-B8CA-4121-A639-6D472D16972A': 'SearchHome',
            '8983036C-27C0-404B-8F08-102D10DCFD74': 'SendTo',
            '7B396E54-9EC5-4300-BE0A-2482EBAE1A26': 'SidebarDefaultParts',
            'A75D362E-50FC-4FB7-AC2C-A8BEAA314493': 'SidebarParts',
            '625B53C3-AB48-4EC1-BA1F-A1EF4146FC19': 'StartMenu',
            'B97D20BB-F46A-4C97-BA10-5E3608430854': 'Startup',
            '43668BF8-C14E-49B2-97C9-747784D784B7': 'SyncManager',
            '289A9A43-BE44-4057-A41B-587A76D7E7F9': 'SyncResults',
            '0F214138-B1D3-4A90-BBA9-27CBC0C5389A': 'SyncSetup',
            '1AC14E77-02E7-4E5D-B744-2EB1AE5198B7': 'System',
            'D65231B0-B2F1-4857-A4CE-A8E7C6EA7D27': 'SystemX86',
            'A63293E8-664E-48DB-A079-DF759E0509F7': 'Templates',
            '5B3749AD-B49F-49C1-83EB-15370FBD4882': 'TreeProperties',
            '0762D272-C50A-4BB0-A382-697DCD729B80': 'UserProfiles',
            'F3CE0F7C-4901-4ACC-8648-D5D44B04EF8F': 'UsersFiles',
            '18989B1D-99B5-455B-841C-AB7C74E4DDFC': 'Videos',
            'F38BF404-1D43-42F2-9305-67DE0B28FC23': 'Windows'}          
        
    rows = []
    diclist = []

    # Row[0]=ETag -- Row[1]=AppId -- Row[2]=AppActivityId -- Row[3]=Activity_type -- Row[4]=ActivityStatus -- Row[5]=Group -- Row[6]=MatchID -- Row[7]=IsInUploadQueue
    # Row[8]=Priority -- Row[9]=ClipboardPayload -- Row[10]=LastModifiedTime -- Row[11]=ExpirationTime -- Row[12]=StartTime -- Row[13]=EndTime -- Row[14]=CreatedInCloud
    # Row[15]=OriginalLastModifiedOnClient -- Row[16]=Tag -- Row[17]=PlatformDeviceId -- Row[18]=Payload
    
    for row in dbdata:
        try:
            #Init all vars as blanks
            strActivityStatus = ""
            strActivityType = ""
            strAppActivityId = ""
            strBackupType = ""
            strBackupUpdated = ""
            strCreationDate = ""
            strCreatedInCloud = ""
            strContent = ""
            strContentUrl = ""
            strCopiedText = ""
            strDescription = ""
            strDeviceIdentifier = ""
            strDeviceName = ""
            strDevicePlatform = ""
            strDeviceType = ""
            strDisplayName  = ""
            strDisplayText = ""
            strDuration = ""
            strEtag = ""
            strEndTime = ""
            strExpirationTime = ""
            strGroup = ""
            strIsInUploadQueue = ""
            strKnownFolder = ""
            strLastModifiedTime = ""
            strMake = ""
            strMatchID = ""
            strModel = ""
            strName = ""
            strNotification = ""
            strObjectId = ""
            strOriginalLastModifiedOnClient = ""
            strPlatformDeviceId = ""
            strPriority = ""
            strStartTime = ""
            strSynched = ""
            strTag = ""
            strTimeZone = ""
            strType = ""
            strVolumeID = ""
            
            ## Fill data ##
            strEtag = row[0]
            strAppActivityId = row[2]
            strActivityStatus = row[4]
            strGroup = row[5]
            strMatchID = row[6]
            strIsInUploadQueue = row[7]
            strPriority = row[8]
            strLastModifiedTime = row[10]
            strExpirationTime = row[11]
            strStartTime = row[12]
            strCreatedInCloud = row[14]
            strOriginalLastModifiedOnClient = row[15]
            strTag = row[16]
            strPlatformDeviceId = row[17]
            
            if row[18]:
                if row[3] == 6:
                    if 'type' in (json.loads(row[18])):
                        strType = (json.loads(row[18]))['type']
                    if 'activeDurationSeconds' in (json.loads(row[18])):
                        strDuration = (json.loads(row[18]))['activeDurationSeconds']
                    if 'userTimezone' in (json.loads(row[18])):
                        strTimeZone = (json.loads(row[18]))['userTimezone']
                    if 'devicePlatform' in (json.loads(row[18])):
                        strDevicePlatform = (json.loads(row[18]))['devicePlatform']

                if row[3] == 5:
                    if 'displayText' in (json.loads(row[18])):
                        strDisplayText = (json.loads(row[18]))['displayText']
                    if 'description' in (json.loads(row[18])):    
                        strDescription = (json.loads(row[18]))['description']
                    if 'appDisplayName' in (json.loads(row[18])):    
                        strDisplayName = (json.loads(row[18]))['appDisplayName']
                    if 'contentUri' in (json.loads(row[18])):
                        strContent = (json.loads(row[18]))['contentUri']
                        
                elif row[3] == 10:
                    strContent = (json.loads(row[18]))['content']  # If error it might be [1]['content'] - Needs B64 decoding, but need example from live database
                    #elseif($item.ActivityType -eq 10){[System.Text.Encoding]::ASCII.GetString([System.Convert]::FromBase64String(($item.Payload|ConvertFrom-Json)."1".content))}

                if row[3] == 2:
                    strNotification = row[18]
            
            if (json.loads(row[1]))[0]['platform'] == "afs_crossplatform":
                strPlatform = (json.loads(row[1]))[1]['platform']
            else:
                strPlatform = (json.loads(row[1]))[0]['platform']
                

            if row[1]:
                if "afs_crossplatform" in (json.loads(row[1]))[0]['platform']:
                    strSynched = "Yes"
            
            if row[3] == 10:
                strCopiedText = base64.b64decode((json.loads(row[9]))[0]['content'])  #Convert from base64
                #$clipboard = if($item.ActivityType -in (10)){[System.Text.Encoding]::ASCII.GetString([System.Convert]::FromBase64String(($item.ClipboardPayload|ConvertFrom-Json).content))}

            acttypelist = [2,3,11,12,15]
            if row[3] in acttypelist: 
                strAppName = (json.loads(row[1]))[0]['application']
            else: 
                if (json.loads(row[1]))[0]['platform'] == "x_exe_path":
                    strAppName = (json.loads(row[1]))[0]['application']
                elif (json.loads(row[1]))[0]['platform'] == "windows_win32":
                    strAppName = (json.loads(row[1]))[0]['application']
                elif (json.loads(row[1]))[0]['platform'] == "windows_universal":
                    strAppName = (json.loads(row[1]))[0]['application']
                elif (json.loads(row[1]))[1]['platform'] == "x_exe_path":
                    strAppName = (json.loads(row[1]))[1]['application']
                elif (json.loads(row[1]))[1]['platform'] == "windows_win32":
                    strAppName = (json.loads(row[1]))[1]['application']
                elif (json.loads(row[1]))[1]['platform'] == "windows_universal":
                    strAppName = (json.loads(row[1]))[1]['application']
                elif (json.loads(row[1]))[2]['platform'] == "x_exe_path":
                    strAppName = (json.loads(row[1]))[2]['application']
                elif (json.loads(row[1]))[2]['platform'] == "windows_win32":
                    strAppName = (json.loads(row[1]))[2]['application']
                elif (json.loads(row[1]))[2]['platform'] == "windows_universal":
                    strAppName = (json.loads(row[1]))[2]['application']

                # Replace app guid with name from the known list        
                for k,v in known.items():
                    y = strAppName.split(k)
                    strAppName = v.join(y)

                # Output "" if date is 1970            
                if row[13] == '1970-01-01 01:00:00':
                    strEndTime = ""
                else:
                    strEndTime = row[13]
                
                if row[3] == 5 and strContent: #if activitytype 5 and data in payload
                    rxuri = re.compile("^file://(.*?)\?")
                    resulturi = rxuri.search(strContent)
                    if resulturi is not None:
                        strContentUrl = resulturi.group(0)
                        strContentUrl = strContentUrl.rstrip("?")
                    
                    rxvolid = re.compile("VolumeId={(.*?)}")
                    resultvolid = rxvolid.search(strContent)
                    if resultvolid is not None:
                        strVolumeID = resultvolid.group(1)
                    
                    rxobjid = re.compile("ObjectId={(.*?)}")
                    resultobjit = rxobjid.search(strContent)
                    if resultobjit is not None:
                        strObjectId = resultobjit.group(1)

                    rxknownfolder = re.compile("KnownFolderId=(.*?)\&")
                    resultknownfolder = rxknownfolder.search(strContent)
                    if resultknownfolder is not None:
                        strKnownFolder = resultknownfolder.group(1)
        
                if strContentUrl and strContent:
                    strContent = strContentUrl

                if row[3] == 3 and row[18]:
                    if 'backupType' in (json.loads(row[18])):
                        strBackupType = (json.loads(row[18]))['backupType']
                    if 'deviceName' in (json.loads(row[18])):
                        strDeviceName = (json.loads(row[18]))['deviceName']
                    if 'deviceIdentifier' in (json.loads(row[18])):
                        strDeviceIdentifier = (json.loads(row[18]))['deviceIdentifier']
                    if 'creationDate' in (json.loads(row[18])):
                        strCreationDate = (json.loads(row[18]))['creationDate']
                    if 'updateDate' in (json.loads(row[18])):
                        strBackupUpdated = (json.loads(row[18]))['updateDate']

                if row[3] == 2:
                    strActivityType = "Notification (2)"
                elif row[3] == 3:
                    strActivityType = "Mobile Device Backup (3)"
                elif row[3] == 5:
                    strActivityType = "Open App/File/Page (5)"
                elif row[3] == 6:
                    strActivityType = "App In Use/Focus (6)"
                elif row[3] == 10:
                    strActivityType = "Clipboard Text (10)"
                elif row[3] == 11:
                    strActivityType = "System " + row[3]
                elif row[3] == 12:
                    strActivityType = "System " + row[3]
                elif row[3] == 15:
                    strActivityType = "System " + row[3]
                elif row[3] == 16:
                    strActivityType = "Copy/Paste (16)"
                else:
                    strActivityType = row[3]
        except:
            continue


        diclist.append({
            'Etag':strEtag, 
            'App_name':strAppName, 
            'DisplayName':strDisplayName,
            'DisplayText':strDisplayText,
            'Description':strDescription,
            'AppActivityId':strAppActivityId,
            'Content':strContent,
            'VolumeID':strVolumeID,
            'ObjectId':strObjectId,
            'KnownFolder':strKnownFolder,
            'Group':strGroup,
            'MatchID':strMatchID,
            'Tag':strTag,
            'Type':strType,
            'ActivityType':strActivityType,
            'ActivityStatus':strActivityStatus,
            'DevicePlatform':strDevicePlatform,
            'Platform':strPlatform,
            'IsInUploadQueue':strIsInUploadQueue,
            'Synched':strSynched,
            'Priority':strPriority,
            'CopiedText':strCopiedText,
            'Notification':strNotification,
            'Duration':strDuration,
            #'CalculatedDuration':strCalculatedDuration,
            'LastModifiedTime':strLastModifiedTime,
            'ExpirationTime':strExpirationTime,
            'StartTime':strStartTime,
            'EndTime':strEndTime,
            'CreatedInCloud':strCreatedInCloud,
            'OriginalLastModifiedOnClient':strOriginalLastModifiedOnClient,
            'TimeZone':strTimeZone,
            'PlatformDeviceId':strPlatformDeviceId,
            'DeviceType':strDeviceType,
            'Name':strName,
            'Make':strMake,
            'Model':strModel,
            'DeviceModel':strDeviceName,
            'DeviceID':strDeviceIdentifier,
            'BackupType':strBackupType,
            'BackupCreated':strCreationDate,
            'BackupUpdated':strBackupUpdated})
        
    # Define Dataframe
    df = pd.DataFrame(diclist)
    # Set datetime format and UTC
    df['StartTime'] = pd.to_datetime(df['StartTime'],utc=True)
    df['EndTime'] = pd.to_datetime(df['EndTime'],utc=True)
    df['LastModifiedTime'] = pd.to_datetime(df['LastModifiedTime'],utc=True)
    df['ExpirationTime'] = pd.to_datetime(df['ExpirationTime'],utc=True)
    df['CreatedInCloud'] = pd.to_datetime(df['CreatedInCloud'],utc=True)

    df['Duration'] = pd.to_numeric(df['Duration'])

    if only_gen_main:
        df.to_csv(outfolder+'gen_report_exported_database.csv', index = False)
        print("Succesfully exported full raw database report")

    else:
        df.to_csv(outfolder+'gen_report_exported_database.csv', index = False)
        print("Succesfully exported full raw database report")
        # Get TimeZone Name to set
        timezonedf = df['TimeZone']
        timezone = timezonedf.dropna().iloc[0]

        # Convert to the users Timezone
        df['StartTime'] = df['StartTime'].dt.tz_convert(timezone)
        df['EndTime'] = df['EndTime'].dt.tz_convert(timezone)
        df['LastModifiedTime'] = df['LastModifiedTime'].dt.tz_convert(timezone)
        df['ExpirationTime'] = df['ExpirationTime'].dt.tz_convert(timezone)
        df['CreatedInCloud'] = df['CreatedInCloud'].dt.tz_convert(timezone)
        
        ##### REPORT GEN #####
        # Report to show when the user is active
        # Export user start and end activity per day

        d = defaultdict(list)

        # Get StartTime Column from the dataframe
        temp = df['StartTime'].astype(str).tolist()

        # Get EndTime Column from the dataframe
        temp2 = df['EndTime'].astype(str).tolist()

        #Combine StartTime and EndTime into a new list
        temp3 = temp + temp2

        # Remove the NaT word from the list
        datelist = list(filter(lambda a: a != "NaT", temp3))

        for dte in datelist:
            key, _ = dte.split()
            d[key].append(dte)

        # Find min and max
        with open(outfolder+'gen_report_useractivity_start_and_end.csv', 'w', newline='\n') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['First Time Entry', 'Last Time Entry'])
            for k,v in d.items():
                csvwriter.writerow((min(v), max(v)))
                
        # Sort the csv and output it
        csvData = pd.read_csv(outfolder+"gen_report_useractivity_start_and_end.csv", parse_dates=['First Time Entry','Last Time Entry'])
        csvData.sort_values(["First Time Entry"], 
                            axis=0,
                            ascending=[False], 
                            inplace=True)
            
        csvData.to_csv(outfolder+'gen_report_useractivity_start_and_end.csv', index = False)
        print('Report gen_report_useractivity_start_and_end.csv Generated successfully')


        ##### REPORT GEN #####
        # Report for When Applications are launched and details
        # Sorted on start time
        # StartTime, App_name, DisplayName, DisplayText, Description
        selection_openapp = df[ df['ActivityType'] == 'Open App/File/Page (5)']
        dg_procname_start = selection_openapp.copy()
        dg_procname_start = dg_procname_start[['StartTime','App_name','DisplayName','DisplayText','Description']]
        dg_procname_start.sort_values(by=['StartTime'],inplace=True, ascending=False)
        dg_procname_start.to_csv(outfolder+'gen_report_ApplicationLaunch_StartTime.csv', index = False)
        print('Report gen_report_ApplicationLaunch_StartTime.csv Generated successfully')


         ##### REPORT GEN #####
        # TXT file that contains all the unique paths found in the database
        # Description, AppActivityId, Content
        dg_paths = df.copy()
        dg_paths = dg_paths[['Description','AppActivityId','Content']]
        
        temppath1 = df['Description'].astype(str).tolist()
        temppath2 = df['AppActivityId'].astype(str).tolist()
        temppath3 = df['Content'].astype(str).tolist()
        temppathlist = temppath1 + temppath2 + temppath3

        temppathlist[:] = [x for x in temppathlist if x] # Remove empty lines
        mylist = set()
        for element in temppathlist:
            x = re.search("\w:\\\.*|(http://|https://).*|\{.*\}.*|file://.*|\\\\\\.*\\\.*", element)
            if x:
                mylist.add(x.group())
        myset = set(mylist)
        textfile = open(outfolder+"Paths_Unique.txt", "w", encoding='utf-8')
        for item in myset:
            textfile.write(str(item) + "\n")
        textfile.close()
        print('Paths_Unique.txt Generated successfully')


        ##### REPORT GEN #####
        # Most used Applications
        # Lists out application and how long it has been actively in use in seconds

        # # Only select rows related to usage
        selection_activeapps = df[ df['ActivityType'] == 'App In Use/Focus (6)']

        # # Copy dataframe
        active_apps = selection_activeapps.copy()
        active_apps = active_apps[['App_name','DisplayName','Duration']]

        # Sum the Activity column
        active_apps = active_apps.groupby('App_name').sum().groupby(level=[0]).cumsum()
        active_apps.sort_values(by=['Duration'],inplace=True, ascending=False)
        active_apps.to_csv(outfolder+'gen_report_Activity_Applications.csv')
        print('Report gen_report_Activity_Applications.csv Generated successfully')


        # ##### CHART GEN #####
        # # HEATMAP For user Activity
        # # Chart that shows when the user starts his day and stops

        # # Only get app in use activites
        adf = df[df['ActivityType'] == "App In Use/Focus (6)"].copy()

        # Add day column
        adf['day'] = adf['StartTime'].dt.day_name()

        # Add hour column
        adf['hour'] = adf['StartTime'].dt.hour

        # Sort weekdays
        weekdays_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        adf.day = pd.Categorical(adf.day,categories=weekdays_order)
        
        # Generate pivot table from data
        heatmap_data = pd.pivot_table(adf, values='Duration', index='day', columns='hour')

        # # Use Pivot table in heatmap
        sns.heatmap(heatmap_data, cmap="cool")
        plt.xlabel("Hour", size=24)
        plt.ylabel("Day", size=7)
        plt.title("User Activity (user's Timezone)", size=14)
        plt.tight_layout()

        # # Output heatmap to jpg file
        plt.savefig(outfolder+'gen_fig_useractivity_heatmap.jpg',dpi=300)
        print('Chart gen_fig_useractivity_heatmap.jpg Generated successfully')

        # ##### CHART GEN #####
        # # Chart that shows when user is active
        df1 = pd.DataFrame()
        df1['Date'] = df['StartTime'].dt.strftime('%Y-%m-%d')

        df1['StartTime'] = df['StartTime'].dt.strftime('%H%M')
        df1['EndTime'] = df['EndTime'].dt.strftime('%H%M')
        df1.EndTime.fillna(df1.StartTime, inplace=True)
        df1['FirstActivityStart'] = df1.groupby('Date')['StartTime'].transform('min').astype(int)
        df1['LastActivityStart'] = df1.groupby('Date')['EndTime'].transform('max').astype(int)
        df1['Filler'] = 2400

        del df1['StartTime']
        del df1['EndTime']
        df1 = df1.sort_values(by='Date', ascending=True)
        df1.drop_duplicates(inplace=True)
        df1 = df1.reset_index(drop=True)
        fig = plt.figure()
        ax1 = fig.add_axes([0,0,1,1])
        ax1.bar(df1['Date'],df1['FirstActivityStart'], color = '#004c6d', width = 0.35, zorder=3)
        ax1.bar(df1['Date'],df1['LastActivityStart'], color = '#5cceff', width = 0.35, zorder=2)
        ax1.bar(df1['Date'],df1['Filler'], color = '#004c6d', width = 0.35, zorder=1)

        ax1.legend(labels=['Idle', 'Active'])
        ax1.set_xticklabels(df1['Date'], rotation=90)
        fig.savefig(outfolder+'gen_fig_useractivity_bar.jpg', bbox_inches='tight',dpi=300)
        print('Chart gen_fig_useractivity_bar.jpg Generated successfully')

        # ##### CHART GEN #####
        # # Most used Applications
        # # Lists out application and how long it has been actively in use in seconds
        top10 = active_apps.head(10)
        plot = top10.plot.pie(y='Duration', figsize=(5, 5), legend=False, title="Top 10 Applications", ylabel='')
        plt.savefig(outfolder+'gen_fig_top10_apps_pie.jpg', bbox_inches='tight',dpi=300)
        print('Chart gen_fig_top10_apps_pie.jpg Generated successfully')

        plot = top10.plot.barh(y='Duration', figsize=(5, 5), legend=False, title="Top 10 Applications", ylabel='')
        plt.savefig(outfolder+'gen_fig_top10_apps_bars.jpg', bbox_inches='tight',dpi=300)
        print('Chart gen_fig_top10_apps_bars.jpg Generated successfully')
