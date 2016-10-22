
CPPFLAGS = -I./include
CFLAGS = 
LDFLAGS = -L./lib -L./lib64
LIBS = -lbsapi

Enroll: enroll.c
	$(CC) $(CPPFLAGS) $(CFLAGS) $(LDFLAGS) enroll.c -o Enroll $(LIBS)

Verify: verify.c
	$(CC) $(CPPFLAGS) $(CFLAGS) $(LDFLAGS) verify.c -o Verify $(LIBS)

