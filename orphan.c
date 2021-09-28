#include <stdio.h>
#include<unistd.h>
#include<sys/wait.h>

int main()
{
    pid_t p;
    p=fork();
    if(p==0){
        sleep(5);
        printf("child: %d",getpid()); 
        printf("parent: %d",getppid()); 
    }
    else{       
        printf("parent: %d",getpid()); 
        printf("child: %d",p);
    }  
}