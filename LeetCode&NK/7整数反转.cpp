#include<iostream>
#include<vector>

int reverse(int x){

    long result=0;//记录结果
    if(x==INT_MIN){//判断下界限
        return 0;
    }
    if(x<0){//为负数的情况
        return int(-reverse(-x));
    }
    int temp=0;
    while(x>0){//进行数据转换
        temp=x%10;
        result=result*10+temp;
        x=x/10;
    }
    if(result>INT_MAX){//判断上界
        return 0;
    }
    return int(result);
}

int main(){

}