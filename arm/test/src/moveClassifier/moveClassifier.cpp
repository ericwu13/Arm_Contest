
#include <vector>
#include <cmath>
#include <float.h>
#include "moveClassifier.h"
#include "../util/dtw.h"
#include "../util/point.h"

using namespace std;

MoveClassifier::MoveClassifier(const float& threshold): _threshold(threshold){
  this->read();
}

string MoveClassifier::operator()(vector<Point>& target){
  int result = 0;
  float loss = FLT_MAX;
	DTW dtw(0.3);
  for(int i = 0;i < _data.size(); ++i){
    float value = dtw.fastdynamic(target, _data[i].data());
    if( value < loss ){
      loss = value;
      result = i;
    };
  };

  if(loss != FLT_MAX){
    return _data[result].action();
  }
  else{
    return "noOps";
  };
};

