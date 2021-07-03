#include<iostream>
#include<vector>
using namespace std;
/*
输入：n = 3
输出：[[1,2,3],[8,9,4],[7,6,5]]
*/
class Solution {
public:
    vector<vector<int>> generateMatrix(int n) {
        
        vector<vector<int>> matrix(n,vector<int>(n));
        if(n==0)return matrix;
        
        int l=0,r=n-1;
        int u=0,d=n-1;
        int nums=1;
        while(l<=r&&u<=d)
        {
        for(int i=l;i<=r;i++){
            matrix[u][i]=nums;
            nums++;
        }
        for(int i=u+1;i<=d;i++){
            matrix[i][r]=nums;
            nums++;
        }
        for(int i=r-1;i>=l;i--){
            matrix[d][i]=nums;
            nums++;
        }
        for(int i=d-1;i>=u+1;i--){
            matrix[i][l]=nums;
            nums++;
        }
        l++;
        r--;
        u++;
        d--;
        }
        return matrix;





    }
};