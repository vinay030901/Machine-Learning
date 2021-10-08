#include<iostream>
using namespace std;

#define INF 100

void merge(int arr[],int p,int q,int r)
{
  int n1 = q-p+1;
  int n2 = r-q;
  int L[n1+1];
  int R[n2+1];
  for(int i=0;i<n1;i++)
    L[i] = arr[p+i];

  for(int j=0;j<n2;j++)
    R[j] = arr[q+1+j];

  L[n1] = INF;
  R[n1] = INF;
  int i =0;
  int j =0;
  cout<<endl;
  for(int i =0;i<n1+1;i++)
  {
    cout<<L[i]<<" ";
  }
  cout<<endl;
  for(int i =0;i<n2+1;i++)
  {
    cout<<R[i]<<" ";
  }

  cout<<endl<<p<<" "<<r<<endl;
  cout<<i<<" "<<j<<endl;
  for(int k = p;k<=r;k++)
    {
      if(L[i]<=R[j]){
        arr[k] = L[i];
        i++;
      }
      else
        {
          arr[k] = R[j];
          j++;
        }
    }
    cout<<endl;
    for(int i=0;i<7;i++)
    {
      cout<<arr[i]<<" ";
    }
    cout<<endl;

}

void merge_sort(int arr[],int p,int r)
{
 if(p<r){
 int q=p+(r-p)/2;
 merge_sort(arr,p,q);
 merge_sort(arr,q+1,r);
 merge(arr,p,q,r);
 }
}

int main()
{
  int n;
  cout<<"Enter size of the array";
  cin>>n;
  int arr[n];

  cout<<"Enter elements in the array:";
  for(int i=0;i<n;i++)
  cin>>arr[i];

  merge_sort(arr,0,n-1);

cout<<endl<<"\t"<<endl;
  for(int i =0;i<n;i++)
  cout<<arr[i]<<" ";

  return 0;
}