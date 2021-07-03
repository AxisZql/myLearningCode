#include<iostream>
#include<vector>
using namespace std;

class Solution {
   
    int index=0;
    int pos=0;
public:
    vector<int> spiralOrder(vector<vector<int>>& matrix) {
             //此题可以采用分而治之的思想一层一层的对矩阵的每一层进行遍历
        if(matrix.size()==0||matrix[0].size()==0)return {};
        int m=matrix.size();
        int n=matrix[0].size();
        int left=0;
        int right=n-1;
        int up=0;
        int down=m-1;
        vector<int> ans;
        vector<vector<bool>> label(m,vector<bool>(n,false));
        CreateAns(matrix,left,right,up,down,ans,label);
        return ans;
    }
        void CreateAns(vector<vector<int>>& matrix,int l,int r,int u,int d,vector<int> &ans,vector<vector<bool>>&label)
    {
        while(l<=r&&u<=d){

         for(int i=l;i<=r;i++){

             if(!label[u][i])
            ans.push_back(matrix[u][i]);
            label[u][i]=true;
            
        }
        // pos=index-1;
        for(int i=u+1;i<=d;i++)
        {    if(!label[i][r])
            ans.push_back(matrix[i][r]);
            label[i][r]=true;
        
        }
        // pos=index-1;
        for(int i=r-1;i>=l;i--)
        {
            if(!label[d][i])
            ans.push_back(matrix[d][i]);
            label[d][i]=true;
        
        }
        // pos=index-1;
        for(int i=d-1;i>u;i--){
             if(!label[i][l])
            ans.push_back(matrix[i][l]);
            label[i][l]=true;
        }
        l++;
        r--;
        u++;
        d--;
    }
 }
};