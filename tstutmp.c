#include <string.h>
#include <utmp.h>
#include <time.h>
#include <stdio.h>

int main(int argc, char **argv)
{
    struct utmp *u;

    setutent();
    while ((u = getutent()) != NULL)
    {
        char *h = (strlen(u->ut_host) == 0) ? "no-host" : u->ut_host;
        char *user = (strlen(u->ut_user) == 0) ? "no-user" : u->ut_user;
        printf("%d %20s %10s %s", u->ut_type, h, user, ctime(&(u->ut_tv.tv_sec)));
    }

    endutent();
}

