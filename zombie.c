#include <stdio.h>
#include<unistd.h>
#include<sys/types.h>
int main()
{
    pid_t p;
    p=fork();
    if(p==0){
        printf("child: %d",getpid()); 
        printf("parent: %d",getppid()); 
    }
    else if(p>0){
        wait(NULL);
        sleep(60);
        printf("parent: %d",getpid()); 
        printf("grand parent: %d",getppid());
    }
    else{
        printf("process not created");
    }
}