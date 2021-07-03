#include<iostream>
#include<vector>
using namespace std;
/*
所谓动态规划就是记录前面已经做过的工作结果，避免出现重复计算
*/

/**
 * 
 * 动态规划+二分法
*/


class Solution {
public:
    /**
     * retrun the longest increasing subsequence
     * @param arr int整型vector the array
     * @return int整型vector
     */
    vector<int> LIS(vector<int>& arr) {
        // write code here
         
        if(arr.size()<=1) return arr; 
        vector<int> dp(arr.size(),1);
        vector<int> maxEnd(1,arr[0]);
        for(int i=1;i<arr.size();i++){
            if(arr[i]>maxEnd.back()){
                dp[i]=maxEnd.size()+1;
                maxEnd.push_back(arr[i]);
            }
            else {
                //查找出第一个大于等于arr[i]数据的位置
                auto pos=std::lower_bound(maxEnd.begin(),maxEnd.end(),arr[i]);
                int idx=pos-maxEnd.begin();
                maxEnd[idx]=arr[i];
                dp[i]=idx+1;//这时候i位置的最长递增子序列即为插入位置的下标+1
            }
        }
            int len=maxEnd.size();
            vector<int> ans(len);
            for(int i=dp.size()-1;i>=0;i--){
                if(dp[i]==len){
                    ans[len-1]=arr[i];
                    len--;
                }
            }
            return ans;
       
    }
};
int main(){

}