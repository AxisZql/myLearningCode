#include<iostream>
#include<vector>
using namespace std;
class Solution {
public:
    /**
     * 代码中的类名、方法名、参数名已经指定，请勿修改，直接返回方法规定的值即可
     *
     * 如果目标值存在返回下标，否则返回 -1
     * @param nums int整型vector 
     * @param target int整型 
     * @return int整型
     
     一定要考虑到存在重复数据的问题，因为题目要求输出的是第一个符合要求的数据
     */
    int search(vector<int>& nums, int target) {
        // write code here
        int low=0;
        int high=nums.size()-1;
        while(low<=high){
            int mid=(low+high)/2;
            if(nums[mid]==target){
               while(mid!=0&&(nums[mid-1]==nums[mid]))
               {
                   --mid;
               }
                return mid;
            }
            if(nums[mid]>target){
                high=mid-1;
            }
            else if(nums[mid]<target)
            {
                low=mid+1;
            }
           
    }
        return -1;
    }
};
int main(){

}