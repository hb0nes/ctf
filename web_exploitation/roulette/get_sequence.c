#include <stdio.h>      
#include <stdlib.h>    
#include <time.h>     
#include <iostream>
#include <limits>
#include <string>
#include <sstream>

void seed(){
    int seed;
    std::cin>>seed;
    srand(seed);
}

int main()
{
    seed();
    int seqNr;
    std::stringstream ss;
    for (int i=1;i<=4;i++){
        seqNr = (rand() % 36) + 1;  
        ss << seqNr << ' ';
        rand();
    }
    std::cout << ss.str() << std::endl;
    return 0;
}
