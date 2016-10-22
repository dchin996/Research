/* 2008-2009 (C) Upek, inc.
 * BSAPI sample Biometry
 * 
 * This sample shows how to manage set of templates in memory. It allows to 
 * add new templates into the set (enroll), delete a finger from the template 
 * set and match finger against the template set or one finger from it.
 *
 * Real application could store the templates in database and make other 
 * complex things.
 */
 

#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <string.h>
#include <sys/types.h>
#include <dirent.h>
#include <errno.h>


#if defined __APPLE__  &&  defined __MACH__
    #include <BSApi/bsapi.h>  /* Mac OS X */
#else
    #include <bsapi.h>  /* other OSes */ 
#endif

 
/* Used to supress compiler warnings */
#ifndef UNREFERENCED_PARAMETER
    #define UNREFERENCED_PARAMETER(param)   (void)param
#endif
 
 
/* Writes info about last error.
 */
static void
status_info(ABS_STATUS status)
{
    ABS_DWORD code;
    const ABS_CHAR* message;
    
    if(status == ABS_STATUS_OK)
        return;
    
    /* ABSGetLastErrorInfo() provides some diagnostical informations
     * about the last BSAPI error which occured in the current thread.
     *
     * Please note that in real applications these informations are 
     * not intended for end user. 
     */
    ABSGetLastErrorInfo(&code, &message);
    printf("   status: %ld\n", (long)status);
    printf("   code:   %ld\n", (long)code);
    printf("   message: '%s'\n", message);
}

 
/* Callback is the primary way how the interactive biometric operations 
 * can interract with the user. Each BSAPI function which expects user 
 * to interact with the fingerprint sensor, takes poitner to structure
 * ABS_OPERATION as a parameter. One of its members is poitner to a 
 * function.
 *
 * BSAPI uses the function as a communication channel between the biometry
 * logic and user. 
 *
 * The callback is the way how to bind the biometry to GUI in your 
 * applications.
 */
static void BSAPI
callback(const ABS_OPERATION* p_operation, ABS_DWORD msg, void* data)
{
    UNREFERENCED_PARAMETER(p_operation);
    
    switch(msg) {
        /* These messages just inform us how the interactive operation
         * progresses. Typical applications do not need it. */
        case ABS_MSG_PROCESS_BEGIN:
        case ABS_MSG_PROCESS_END:
            break;
            
        /* On some platforms, the biometric operastion can be suspended
         * when other process acquires sensor for other operation. */
        case ABS_MSG_PROCESS_SUSPEND:
            printf("   operation has been suspended\n");
            break;
        case ABS_MSG_PROCESS_RESUME:
            printf("   operation has been resumed\n");
            break;
            
        /* Sometimes some info how the operation progresses is sent. */
        case ABS_MSG_PROCESS_PROGRESS:
        {
            ABS_PROCESS_PROGRESS_DATA* progress_data = 
                                    (ABS_PROCESS_PROGRESS_DATA*) data;
            if(progress_data->Percentage <= 100) {
                printf("   operation in progress (%d%%)...\n", 
                                            (int)progress_data->Percentage);
            } else {
                printf("   operation in progress...\n");
            }
            break;
        }
        case ABS_MSG_PROCESS_SUCCESS:
            printf("   success\n");
            break;
        case ABS_MSG_PROCESS_FAILURE:
            printf("   failure\n");
            break;
        
        /* Prompt messages should inform the user that he should do 
         * something. */
        case ABS_MSG_PROMPT_SCAN:
            printf("   swipe the finger\n"); 
            break;
        case ABS_MSG_PROMPT_TOUCH:
            printf("   touch the sensor\n");
            break;
        case ABS_MSG_PROMPT_KEEP:
            printf("   keep finger on the sensor\n"); 
            break;
        case ABS_MSG_PROMPT_LIFT:
            printf("   lift your finger away from the sensor\n");
            break;
        case ABS_MSG_PROMPT_CLEAN:
            printf("   clean the sensor\n"); 
            break;
        
        /* Quality messages come if something went wrong. E.g. the user
         * did not scan his finger in the right way. */
        case ABS_MSG_QUALITY_CENTER_HARDER:
            printf("   bad quality: center and harder\n"); 
            break;
        case ABS_MSG_QUALITY_CENTER:
            printf("   bad quality: center\n"); 
            break;
        case ABS_MSG_QUALITY_TOO_LEFT:
            printf("   bad quality: too left\n"); 
            break;
        case ABS_MSG_QUALITY_TOO_RIGHT:
            printf("   bad quality: too right\n"); 
            break;
        case ABS_MSG_QUALITY_HARDER:
            printf("   bad quality: harder\n"); 
            break;
        case ABS_MSG_QUALITY_TOO_LIGHT:
            printf("   bad quality: too light\n"); 
            break;
        case ABS_MSG_QUALITY_TOO_DRY:
            printf("   bad quality: too dry\n");
            break;
        case ABS_MSG_QUALITY_TOO_SMALL:
            printf("   bad quality: too small\n");
            break;
        case ABS_MSG_QUALITY_TOO_SHORT:
            printf("   bad quality: too short\n"); 
            break;
        case ABS_MSG_QUALITY_TOO_HIGH:
            printf("   bad quality: too high\n"); 
            break;
        case ABS_MSG_QUALITY_TOO_LOW:
            printf("   bad quality: too low\n"); 
            break;
        case ABS_MSG_QUALITY_TOO_FAST:
            printf("   bad quality: too fast\n"); 
            break;
        case ABS_MSG_QUALITY_TOO_SKEWED:
            printf("   bad quality: too skewed\n"); 
            break;
        case ABS_MSG_QUALITY_TOO_DARK:
            printf("   bad quality: too dark\n"); 
            break;
        case ABS_MSG_QUALITY_BACKWARD:
            printf("   bad quality: backward movement detected\n"); 
            break;
        case ABS_MSG_QUALITY_JOINT:
            printf("   bad quality: joint detected\n"); 
            break;
        
        /* Navigation messages are sent only from ABSNavigate. Its not used
         * in this sample but we list the messages here for completeness. */
        case ABS_MSG_NAVIGATE_CHANGE:
        case ABS_MSG_NAVIGATE_CLICK:
            break;
            
        /* Real application would probably use some GUI to provide feedback
         * for user. On these messages the GUI dialog should be made vsiible
         * and invisible respectivelly. */
        case ABS_MSG_DLG_SHOW:
        case ABS_MSG_DLG_HIDE:
            break;
            
        /* Idle message can come only if flag ABS_OPERATION_FLAG_USE_IDLE
         * was specified in ABS_OPERATION::dwFlags (i.e. never in this sample).
         * If the flag is specified, this message comes very often, hence 
         * giving the callback a chance to cancel the operation with 
         * ABSCancelOperation() without long time delays. In multithreaded 
         * applications, canceling the operation from another thread can be
         * better alternative. Consult BSAPI documentation for more info about
         * the topic. */
        case ABS_MSG_IDLE:
            break;
    }
}


/* Maximal template set size. */
#define TSET_SIZE        16

/* We use trivial template set representation, as an array of pointers 
 * to ABS_BIR. Unused slots are set to NULL. */
static ABS_BIR* tset[TSET_SIZE];

/* 0 - BIR was obtained via a ABS_* call (and thus should be freed
 *     by ABSFree()),
 * 1 - BIR was created manually and should be freed with free(). */
static char tsetAttr[TSET_SIZE];

/* BSAPI session handle. */
static ABS_CONNECTION conn = 0;



/* Pointer to ABS_OPERATION is taken as a parameter by those BSAPI 
 * funtions which work as interactive operation. The main purpose of it is 
 * to pass pointer to the callback function into the interactive functions. 
 *
 * It also allows to specifie some flags and/or timeout.
 *
 * In this sample we reuse this one operation instance. In real complex 
 * application you may need to use special ABS_OPERATION instance for 
 * each BSAPI interactive operation. This allows you to use specialized
 * callback for them, past various flags etc.
 */
static ABS_OPERATION op = { 
    /* ID of the operation. We don't need to identify the operation in this 
     * sample. When non-zero, the ID identifies the operation and allows it
     * to be canceled from any other thread with ABSCancelOperation(). */
    0,         
    
    /* Arbitrary pointer, which allows application to pass any data into
     * the callback. Not used in this sample. */
    NULL,      
    
    /* Pointer to a simple callback implementation function. */
    callback,  
    
    /* Timeout. For example, lets set timeout to 60 sec. Note the value does 
     * not limit how long the operation (e.g. ABSVerify()) can take. The 
     * timeout only specifies time the operation waits for user to put his 
     * finger on a sensor. Zero would mean no timeout (i.e. the operation can 
     * never end if user never puts his finger on the sensor.) */
    60000,
    
    /* By default BSAPI places short time delays between sending some important
     * callback messages. The purpose of this is to guarantee that if multiple
     * messages come very closely in sequence, then the user still has enough
     * time to see all the messages and not just the lat one of the fast
     * sequence.
     *
     * For application developer, this simplifies callback implementation
     * which in most cases can be just showing an appropriate message in a 
     * window or dialog.
     *
     * However the time delays are not needed when user can see all history
     * of the messages, e.g. (as in this sample) the messages are outputted
     * to standard output stream. Hence we disable the time delays with with 
     * the flag ABS_OPERATION_FLAG_LL_CALLBACK here. */
    ABS_OPERATION_FLAG_LL_CALLBACK
};


/* Helper function, asking the user to choose what slot in the template set 
 * to work with. Returns number of the slot or -1 if the slot can not be used.
 */
static int
choose_slot(const char* msg)
{
    int slot;
    
    printf("%s: ", msg);
    scanf("%d", &slot);
    if(slot < 0  ||  slot >= TSET_SIZE) {
        printf("No such slot.\n");
        return -1;
    }
    if(tset[slot] == NULL) {
        printf("Slot %d is not enrolled.\n", slot);
        return -1;
    }
    
    return slot;
}

/* Open BSAPI session. Note that this sample allows only one session
 * at a time to be opened. */
static void 
cmd_open(void)
{
    ABS_STATUS res;
    ABS_DEVICE_LIST* dev_list;
    int dev_index;
    
    printf("Openening a session...\n");
    
    /* Check whether it's not already open. It is possible to use multiple
     * sessions from one process, but it would make this sample much more 
     * copmplex, and most applications do not need that anyway. */
    if(conn != 0) {
        printf("The session is already open.\n");
        return;
    }
    
    /* Enumerate all supported USB devices and decide which one of them to 
     * use. */
    res = ABSEnumerateDevices("usb", &dev_list);
    if(res != ABS_STATUS_OK) {
        printf("ABSEnumerateDevices() failed.\n");
        status_info(res);
        return;
    }
    if(dev_list->NumDevices == 0) {
        printf("No fingerprint device found.\n");
        return;
    }
    if(dev_list->NumDevices == 1) {
        /* There is a single device, so take it. */
        dev_index = 0;
    } else {
        /* There is more then one device connected: Ask user which one
         * of them to use. */
        int i;
        
        printf("Found devices: \n");
        for(i = 0; i < (int)dev_list->NumDevices; i++)
            printf("   %d  %s\n", i, dev_list->List[i].DsnSubString);
        printf("Enter number of device you want to use: ");
        scanf("%d", &dev_index);
        if(dev_index < 0  ||  dev_index >= (int)dev_list->NumDevices) {
            printf("No such device.\n");
            return;
        }
    }
    
    /* Open the selected device. */
    printf("Opening device '%s'...\n", dev_list->List[dev_index].DsnSubString);
    res = ABSOpen(dev_list->List[dev_index].DsnSubString, &conn);
    if(res != ABS_STATUS_OK) {
        ABSFree(dev_list);
        printf("ABSOpen() failed.\n");
        status_info(res);
        return;
    }
    
    /* Release memory allocated for the device list. */
    ABSFree(dev_list);
    
    printf("Opened successfully.\n");
}

/* Close BSAPI session */
static void 
cmd_close(void)
{
    ABS_STATUS res;
    
    printf("Closing the current session...\n");
    
    /* close the connection */    
    res = ABSClose(conn);
    if(res != ABS_STATUS_OK) {
        printf("ABSClose() failed.\n");
        status_info(res);
        return;
    }
    conn = 0;
}

/* Add (enroll) new template into the template set. */
static void
cmd_add(void)
{
    int i;
    int slot = -1;
    ABS_STATUS res;
    
    printf("Add new template...\n");
    
    /* find an empty slot */
    for(i = 0; i < TSET_SIZE; i++) {
        if(tset[i] == NULL) {
            slot = i;
            break;
        }
    }    
    if(slot < 0) {
        printf("Cannot add new template. The template set is full.\n");
        return;
    }
    
    /* enroll the tamplate into the slot */
    res = ABSEnroll(conn, &op, &tset[slot], 0);
    if(res != ABS_STATUS_OK) {
        printf("ABSEnroll() failed.\n");
        status_info(res);
        return;
    }
    
    printf("Successfully enrolled into the template set as slot #%d.\n", slot);
}

/* Import a template from a file into the template set. */
static void
cmd_import(const char* templateFileName)
{
    int i;
    int slot = -1;
    //char templateFileName[1024];
    FILE *f;
    long fileSize;
    
    //printf("Import a template...\n");
    
    /* find an empty slot */
    for(i = 0; i < TSET_SIZE; i++) {
        if(tset[i] == NULL) {
            slot = i;
            break;
        }
    }    
    if(slot < 0) {
        printf("Cannot add new template. The template set is full.\n");
        return;
    }
    
    /* ask user for the filename */
    //printf("Please enter template file name: ");
    //if (scanf("%s", templateFileName) != 1) {
        //printf("Cannot get the file name.\n");
        //return;
    //}
	errno = 0;
    f = fopen(templateFileName, "rb+");
    if (f == NULL) {
        printf("Cannot open file '%s'.\n", templateFileName);
        printf("Error: %d \n", errno);
        return;
    }

    if (fseek(f, 0, SEEK_END) != 0) {
        printf("Cannot seek in file '%s'.\n", templateFileName);
        fclose(f);
        return;
    }

    fileSize = ftell(f);
    if (fileSize < 0) {
        printf("Cannot determine the size of file '%s'.\n", templateFileName);
        fclose(f);
        return;
    }

    if (fseek(f, 0, SEEK_SET) != 0) {
        printf("Cannot seek back in file '%s'.\n", templateFileName);
        fclose(f);
        return;
    }

    tset[slot] = (ABS_BIR*)malloc(fileSize);
    if (tset[slot] == NULL) {
        printf("Cannot allocate %ld bytes.\n", fileSize);
        fclose(f);
        return;
    }

    if (fread(tset[slot], fileSize, 1, f) != 1) {
        printf("Cannot read %ld bytes from file '%s'.\n", fileSize,
            templateFileName);
        free(tset[slot]);
        tset[slot] = NULL;
        fclose(f);
        return;
    }

    tsetAttr[slot] = 1;

    fclose(f);
    //printf("Successfully imported into the template set as slot #%d.\n", slot);
}

/* Export a template from the template set into a file. */
static void
cmd_export(void)
{
    int slot;
    char templateFileName[1024];
    FILE *f;

    //printf("Exporting a template from the template set...\n");

    /* Ask user which templates to compare */
    slot = 0;

    /* ask user for the filename */
    printf("Please enter template file name: ");
    if (scanf("%s", templateFileName) != 1) {
        printf("Cannot get the file name.\n");
        return;
    }

    f = fopen(templateFileName, "wb");
    if (f == NULL) {
        printf("Cannot open file '%s'.\n", templateFileName);
        return;
    }

    if (fwrite(tset[slot], tset[slot]->Header.Length, 1, f) != 1) {
        printf("Cannot write %u bytes to file '%s'.\n",
            tset[slot]->Header.Length, templateFileName);
        fclose(f);
        return;
    }

    fclose(f);
    printf("Successfully exported template to file '%s'.\n",
        templateFileName);
}

/* Remove one slot from the template set */
static void
cmd_delete(void)
{
    int slot;
    
    printf("Delete a template from the template set...\n");
    
    /* Ask user which slot to delete */
    slot = choose_slot("Enter slot number to delete from template set");
    if(slot < 0)
        return;
    
    /* And just do it */
    if (tsetAttr[slot] != 0)
        free(tset[slot]);
    else
        ABSFree(tset[slot]);
    tset[slot] = NULL;
    printf("Successfully deleted slot %d\n", slot);
}

/* Remove all templates stored in the template set */
static void
cmd_delete_all(void)
{
    int i;
    
    printf("Delete all templates from the template set...\n");
    
    /* Remove all templates in the template set */
    for(i = 0; i < TSET_SIZE; i++) {
        if(tset[i] != NULL) {
            if (tsetAttr[i] != 0)
                free(tset[i]);
            else
                ABSFree(tset[i]);
            tset[i] = NULL;
        }
    }
    printf("Successfully deleted all slots\n");
}

/* This function only lists which slots on the template sets are used 
 * (i.e. which contain an enrolled template). */
static void
cmd_list(void)
{
    int i;
    int empty = 1;
    
    printf("Listing which slots are used (enrolled)...\n");
    printf("Enrolled slots: ");
    
    for(i = 0; i < TSET_SIZE; i++) {
        if(tset[i] != NULL) {
            printf("%d ", i);
            empty = 0;
        }
    }
    
    if(empty)
        printf("none\n");
    else
        printf("\n");
}

/* Verify user's finger against one template in the set */
static void 
cmd_verify(void)
{
    int slot;
    ABS_STATUS res;
    ABS_LONG matching_slot;
    
    printf("Verify user's finger against a template in template set...\n");
    
    /* Ask user which template to compare with */
    slot = choose_slot("Enter slot number to match against");
    if(slot < 0)
        return;
    
    /* And just do it. Note that matching_slot is set to index of the 
     * matching slot in the template set or -1 is no one matches. Here 
     * we pass in only the one template we are interested in, so in case of 
     * match it will be zero. */
    res = ABSVerify(conn, &op, 1, &tset[slot], &matching_slot, 0);
    if(res != ABS_STATUS_OK) {
        printf("ABSVerify() failed\n");
        status_info(res);
        return;
    }    
    if(matching_slot == 0) {
        printf("Match\n");
    } else if(matching_slot < 0) {
        printf("No match\n");
    } else {
        /* this never happen */
        assert(0);
    }
}

/* Here we compare the user's finger with all templates stored in the set */
static void
cmd_verify_all(void)
{
    int i;
    ABS_BIR* tmp_tset[TSET_SIZE];
    int tmp_slot[TSET_SIZE];
    ABS_DWORD count = 0;
    ABS_STATUS res;
    ABS_LONG index;
    
    printf("Verify user's finger against all templates in template set...\n");
    
    /* Functions ABSVerify accepts an arbitrary count of templates to verify
     * the scanned finger against. It expects pointers to the templates in an
     * array of pointers to ABS_BIR structures. This matches our template 
     * set representation, however our template set might have some gaps
     * (NULLs) in the array, so we copy the BIR pointers to a temporary array
     * without the gaps (i.e. NULL values can be only on tail of the array). 
     * Therefore we also have to save the original index so we can map the 
     * resulting matching index to the original slot number.
     *
     * During the work we also count how many templates are in the set.
     */
    for(i = 0; i < TSET_SIZE; i++) {
        if(tset[i] != NULL) {
            tmp_tset[count] = tset[i];
            tmp_slot[count] = i;
            count++;
        }
    }
    if(count == 0) {
        printf("The template set is empty.\n");
        return;
    }

    /* Now we can compare the finger against all the templates in the 
     * temporary array */
    res = ABSVerify(conn, &op, count, tmp_tset, &index, 0);
    if(res != ABS_STATUS_OK) {
        printf("ABSVerify() failed\n");
        status_info(res);
        return;
    }
    
    /* Find out the slot number (index in the tset array) */
    if(index >= 0) {
        //printf("Slot %d matches.\n", tmp_slot[index]);
        printf("Match found!\n");
    } else {
        printf("No matches\n");
    }
}

/* Here we compare two templates from the template set */
static void
cmd_verify_match(void)
{
    int slot1, slot2;
    ABS_STATUS res;
    ABS_BOOL match;
    
    printf("Comparing two templates in the template set...\n");
    
    /* Ask user which templates to compare */
    slot1 = choose_slot("Enter slot number of template 1 to compare");
    if(slot1 < 0)
        return;
    slot2 = choose_slot("Enter slot number of template 2 to compare");
    if(slot2 < 0)
        return;
    
    /* Now compare the two templates. Note this is not interactive operation.
     * I.e. the user is not asked to manipulate with the sensor, nor the
     * function takes pointer to ABS_OPERATION. */
    res = ABSVerifyMatch(conn, tset[slot1], tset[slot2], &match, 0);
    if(res != ABS_STATUS_OK) {
        printf("ABSVerifyMatch() failed.\n");
        status_info(res);
        return;
    }
    if(match)
        printf("Templates %d and %d do match.\n", slot1, slot2);
    else
        printf("Templates %d and %d do NOT match.\n", slot1, slot2);
}

/* Writes down simple help. */
static void
cmd_help(void)
{
    printf("Press any of the following keys to do the corresponding action:\n");
    printf("   o ... open BSAPI session\n");
    printf("   c ... close the BSAPI session\n");
    printf("   a ... add new template into the template set\n");
    printf("   i ... import a template into the template set\n");
    printf("   e ... export a template from the template set to a file\n");
    printf("   d ... delete template from the template set\n");
    printf("   D ... delete all templates from the template set\n");
    printf("   l ... list templates in the template set\n");
    printf("   v ... verify finger against one template\n");
    printf("   V ... verify finger against complete template set\n");
    printf("   m ... match two templates from the template set\n");
    printf("   h ... writes down this help message\n");
    printf("   q ... quit this sample program\n");
}

static void
list_directory(
    const char *dirname)
{
    DIR *dir;
    struct dirent *ent;
                
    /* Open directory stream */
    dir = opendir (dirname);
    if (dir != NULL) {

        /* Print all files and directories within the directory */
        printf("Looking in %s...\n", dirname);
        while ((ent = readdir (dir)) != NULL) {
            //printf("%s\n", ent->d_name);
            int size = strlen(ent->d_name);
            char sub_string[256];
            strcpy(sub_string, ent->d_name);
            const char *last_four = &sub_string[size - 5];
            if (strcmp(last_four, ".fing") == 0) {
				char file_name[100];
				strcpy(file_name, dirname);
				strcat(file_name, "/");
				strcat(file_name, ent->d_name);
				cmd_import(file_name);
			}
			
        }
        closedir (dir);
	}
}


int
main(int argc, char** argv)
{
    ABS_STATUS res;
    
    res = ABSInitialize();
    if(res != ABS_STATUS_OK) {
        printf("ABSInitialize() failed\n");
        status_info(res);
        return -1;
    }
    cmd_open();
    // adds all files in this directory to TSET
    list_directory("./Enrolling");
    ABS_BIR* verify_template;
    
    /* enroll the the verification template*/

    cmd_verify_all();
    
    
    
  
    //int i;
    //int done = 0;
    //char buffer[256];
    
    //UNREFERENCED_PARAMETER(argc);
    //UNREFERENCED_PARAMETER(argv);
    
    //printf(
        //"This sample shows BSAPI as it can be used in typical real application\n"
        //"The sample keeps a fingerprint template set in memory and provides\n"
        //"functions for manipulating with the template set as adding new\n"
        //"template into it (enrollment), removing it, various verification\n"
        //"and matching functions.\n"
        //"\n"
        //"Note that when started, it does not open session to the device\n"
        //"automatically so before you can use any command operating with\n"
        //"the fingerprint device you have to open it with 'o'.\n"
        //"\n"
        //"In this regard behavior of the sample may differ from real life\n"
        //"applications which may call ABSOpen() just after ABSInitialize().\n"
        //"\n"
        //"This design was chosen so that you can manually close and reopen\n"
        //"the session, and that you can see which functions require an open\n"
        //"session and which do not.\n"
        //"\n"
    //);
    
    ///* initialize BSAPI */
    //res = ABSInitialize();
    //if(res != ABS_STATUS_OK) {
        //printf("ABSInitilize() failed\n");
        //status_info(res);
        //return -1;
    //}
    
    ///* ensure the template set is empty */
    //for(i = 0; i < TSET_SIZE; i++)
    //{
        //tset[i] = NULL;
        //tsetAttr[i] = 0;
    //}

    ///* On the start, always show the help */
    //cmd_help();

    //while(!done) {
        ///* Ask the use what to do... */
        //printf("\n");
        //printf("\n>> ");
        //scanf("%s", buffer);
        
        ///* ...and then just do that. */
        //switch(buffer[0]) {
            //case 'o': cmd_open(); break;
            //case 'c': cmd_close(); break;
            //case 'a': cmd_add();  break;
            //case 'i': cmd_import();  break;
            //case 'e': cmd_export();  break;
            //case 'd': cmd_delete(); break;
            //case 'D': cmd_delete_all(); break;
            //case 'l': cmd_list(); break;
            //case 'v': cmd_verify(); break;
            //case 'V': cmd_verify_all(); break;
            //case 'm': cmd_verify_match(); break;
            //case 'q': done = 1; break;
            
            //case '?':
            //case 'h': cmd_help(); break;
            
            //default:  
                //printf("Unknown command. Press 'h' to get help.\n"); 
                //break;
        //}
    //}

    ///* Release any templates kept in the template set. */
    //for(i = 0; i < TSET_SIZE; i++) {
        //if(tset[i] != NULL) {
            //if (tsetAttr[i] != 0)
                //free(tset[i]);
            //else
                //ABSFree(tset[i]);
            //tset[i] = NULL;
        //}
    //}
    
    /* If BSAPI session is opened, close it */
    if(conn != 0)
        cmd_close();
    
    /* Free any resources allocated in ABSInitialize. */
    ABSTerminate();
    
    return 0;
}
