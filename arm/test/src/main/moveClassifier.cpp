
#include <iostream>
#include <stdio.h>
#include "../moveClassifier/moveClassifier.h"


using namespace std;

int main(int argc, char *argv[]){
  MoveClassifier classifier(200, 2);
  vector<Point> target;
  for(int i = 0; i < 3; ++i){
    target.push_back(Point(1));
  };
  cout<< classifier(target)<<endl;

  return 0;
}
