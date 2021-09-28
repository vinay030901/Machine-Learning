#include<stdio.h>
#include<unistd.h>
#include<stdlib.h>
#include<sys/types.h>
#include<sys/wait.h>
int main()
{
    int pid;
    int a[30],n,sum=0,i,status;
    printf("enter the number of elements: ");
    scanf("%d",&n);
    printf("enter the elements: ");
    for(i=0;i<n;i++)
    scanf("%d",&a[i]);
    pid=fork();
    wait(&status);
    if(pid==0)
    {
        for(i=0;i<n;i++)
        if(a[i]%2==0)
        sum+=a[i];
        printf("sum of even numbers is: %d",sum);
    }
    else if(pid==1){
        for(i=0;i<n;i++)
        if(a[i]%2!=0)
        sum+=a[i];
        printf("sum of odd numbers is: %d",sum);
    }
    return 0;
}