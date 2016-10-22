"""
The error codes defined by BSAPI, found in bserror.h

"""

# Success return status.
ABS_STATUS_OK = 0

# General, unknown, or unspecified error.
ABS_STATUS_GENERAL_ERROR = -5001

# Internal error.
ABS_STATUS_INTERNAL_ERROR = -5002

# BSAPI has been already initialized.
ABS_STATUS_ALREADY_INITIALIZED = -5003

# BSAPI is not initialized.
ABS_STATUS_NOT_INITIALIZED = -5004

# Connection is already opened.
ABS_STATUS_ALREADY_OPENED = -5005

# Invalid parameter.
ABS_STATUS_INVALID_PARAMETER = -5006

# Invalid (connection) handle.
ABS_STATUS_INVALID_HANDLE = -5007

# No such device found.
ABS_STATUS_NO_SUCH_DEVICE = -5008

# Operation has been interrupted due timeout.
ABS_STATUS_TIMEOUT = -5009

# Requested feature/function not implemented.
ABS_STATUS_NOT_IMPLEMENTED = -5010

# Requested feature/function not supported.
ABS_STATUS_NOT_SUPPORTED = -5011

# The operation has been canceled.
ABS_STATUS_CANCELED = -5012

# The operation has not been found (invalid operation ID or the
# operation already finished).
ABS_STATUS_NO_SUCH_OPERATION = -5013

# Communication error related to remote session (Terminal Services or
# Citrix) has occured.
ABS_STATUS_REMOTE_COMM_ERROR = -5014

# The operation is not permitted. It might be a matter insufficient
# rights of the current user.
ABS_STATUS_ACCESS_DENIED = -5015

error_strings = {
    ABS_STATUS_OK:"",
    ABS_STATUS_GENERAL_ERROR:"unspecified error",
    ABS_STATUS_INTERNAL_ERROR:"internal error",
    ABS_STATUS_ALREADY_INITIALIZED:"BSAPI already initialized",
    ABS_STATUS_NOT_INITIALIZED:"BSAPI not initialized",
    ABS_STATUS_ALREADY_OPENED:"connection already opened",
    ABS_STATUS_INVALID_PARAMETER:"invalid parameter",
    ABS_STATUS_INVALID_HANDLE:"invalid connection handle",
    ABS_STATUS_NO_SUCH_DEVICE:"no such device",
    ABS_STATUS_TIMEOUT:"timeout",
    ABS_STATUS_NOT_IMPLEMENTED:"not implemented",
    ABS_STATUS_NOT_SUPPORTED:"not supported",
    ABS_STATUS_CANCELED:"canceled",
    ABS_STATUS_NO_SUCH_OPERATION:"no such operation",
    ABS_STATUS_REMOTE_COMM_ERROR:"remote communication error",
    ABS_STATUS_ACCESS_DENIED:"access denied"
    }

def check_call(return_code):
    if return_code in error_strings:
        output = error_strings[return_code]
    else:
        output = "unknown error code: {}".format(return_code)
    if output:
        print("Operation failed with error:", output)
        exit(return_code)

# These codes are used as values for dwMsgID parameter of ABS_CALLBACK
ABS_MSG_PROCESS_BEGIN = 0x11000000
ABS_MSG_PROCESS_END = 0x12000000
ABS_MSG_PROCESS_SUSPEND = 0x13000000
ABS_MSG_PROCESS_RESUME = 0x14000000
ABS_MSG_PROCESS_PROGRESS = 0x15000000
ABS_MSG_PROCESS_SUCCESS = 0x16000000
ABS_MSG_PROCESS_FAILURE = 0x17000000
ABS_MSG_PROMPT_SCAN = 0x21000000
ABS_MSG_PROMPT_TOUCH = 0x22000000
ABS_MSG_PROMPT_KEEP = 0x23000000
ABS_MSG_PROMPT_LIFT = 0x24000000
ABS_MSG_PROMPT_CLEAN = 0x25000000
ABS_MSG_QUALITY = 0x30000000
ABS_MSG_QUALITY_CENTER_HARDER = 0x31000000
ABS_MSG_QUALITY_CENTER = 0x31100000
ABS_MSG_QUALITY_TOO_LEFT = 0x31110000
ABS_MSG_QUALITY_TOO_RIGHT = 0x31120000
ABS_MSG_QUALITY_TOO_HIGH = 0x31130000
ABS_MSG_QUALITY_TOO_LOW = 0x31140000
ABS_MSG_QUALITY_HARDER = 0x31200000
ABS_MSG_QUALITY_TOO_LIGHT = 0x31210000
ABS_MSG_QUALITY_TOO_DRY = 0x31220000
ABS_MSG_QUALITY_TOO_SMALL = 0x31230000
ABS_MSG_QUALITY_TOO_SHORT = 0x32000000
ABS_MSG_QUALITY_TOO_FAST = 0x33000000
ABS_MSG_QUALITY_TOO_SKEWED = 0x34000000
ABS_MSG_QUALITY_TOO_DARK = 0x35000000
ABS_MSG_QUALITY_BACKWARD = 0x36000000
ABS_MSG_QUALITY_JOINT = 0x37000000
ABS_MSG_NAVIGATE_CHANGE = 0x41000000
ABS_MSG_NAVIGATE_CLICK = 0x42000000
ABS_MSG_DLG_SHOW = 0x51000000
ABS_MSG_DLG_HIDE = 0x52000000
ABS_MSG_IDLE = 0x0

callback_message_strings = {
    ABS_MSG_PROCESS_BEGIN:None,
    ABS_MSG_PROCESS_END:None,
    ABS_MSG_PROCESS_SUSPEND:"operation has suspended",
    ABS_MSG_PROCESS_RESUME:"operation has been resumed",
    ABS_MSG_PROCESS_PROGRESS:"operation in progress...",
    ABS_MSG_PROCESS_SUCCESS:"successful read",
    ABS_MSG_PROCESS_FAILURE:"failed to read",
    ABS_MSG_PROMPT_SCAN:"swipe the finger",
    ABS_MSG_PROMPT_TOUCH:"touch the sensor",
    ABS_MSG_PROMPT_KEEP:"keep finger on the sensor",
    ABS_MSG_PROMPT_LIFT:"lift your finger away from the sensor",
    ABS_MSG_PROMPT_CLEAN:"clean the sensor",
    ABS_MSG_QUALITY:"bad quality (unknown problem)",
    ABS_MSG_QUALITY_CENTER_HARDER:"bad quality: center and harder",
    ABS_MSG_QUALITY_CENTER:"bad quality: center",
    ABS_MSG_QUALITY_TOO_LEFT:"bad quality: too left",
    ABS_MSG_QUALITY_TOO_RIGHT:"bad quality: too right",
    ABS_MSG_QUALITY_TOO_HIGH:"bad quality: too high",
    ABS_MSG_QUALITY_TOO_LOW:"bad quality: too low",
    ABS_MSG_QUALITY_HARDER:"bad quality: harder",
    ABS_MSG_QUALITY_TOO_LIGHT:"bad quality: too light",
    ABS_MSG_QUALITY_TOO_DRY:"bad quality: too dry",
    ABS_MSG_QUALITY_TOO_SMALL:"bad quality: too small",
    ABS_MSG_QUALITY_TOO_SHORT:"bad quality: too short",
    ABS_MSG_QUALITY_TOO_FAST:"bad quality: too fast",
    ABS_MSG_QUALITY_TOO_SKEWED:"bad quality: too skewed",
    ABS_MSG_QUALITY_TOO_DARK:"bad quality: too dark",
    ABS_MSG_QUALITY_BACKWARD:"bad quality: backward",
    ABS_MSG_QUALITY_JOINT:"bad quality: joint detected",
    ABS_MSG_NAVIGATE_CHANGE:None,
    ABS_MSG_NAVIGATE_CLICK:None,
    ABS_MSG_DLG_SHOW:None,
    ABS_MSG_DLG_HIDE:None,
    ABS_MSG_IDLE:None
    }
    
def callback_message(code):
    return callback_message_strings[code]
