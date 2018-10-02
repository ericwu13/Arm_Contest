#include <iostream>
#include <cmath>
#include <vector>
#include <string>
#include <sstream>
#include "string.h"
#include <iostream>
#include <algorithm>
//#include <stdexcept>
#include "dtw.h"
using namespace std;

SimpleDTW::SimpleDTW()
{
    distance_fn_ = NULL;
    initialized_ = false;
}

SimpleDTW::SimpleDTW(size_t x_size, size_t y_size, double (*distance_fn)(vector<double> p1, vector<double> p2))
{
    distance_fn_ = distance_fn;
    SimpleDTW::Initialize(x_size, y_size);
}

SimpleDTW::SimpleDTW(double (*distance_fn)(vector<double> p1, vector<double> p2))
{
    distance_fn_ = distance_fn;
    initialized_ = false;
}

void SimpleDTW::Initialize(size_t x_size, size_t y_size)
{
    x_dim_ = x_size + 1;
    y_dim_ = y_size + 1;
    // Resize the data
    data_.resize(x_dim_ * y_dim_, 0.0);
    //Populate matrix with starting values
    SetInDTWMatrix(0, 0, 0.0);
    for (size_t i = 1; i < x_dim_; i++)
    {
        SetInDTWMatrix(i, 0, INFINITY);
    }
    for (size_t i = 1; i < y_dim_; i++)
    {
        SetInDTWMatrix(0, i, INFINITY);
    }
    initialized_ = true;
}

double SimpleDTW::EvaluateWarpingCost(vector< vector<double> > sequence_1, vector< vector<double> > sequence_2)
{
    // Sanity checks
    if (sequence_1.size() == 0 || sequence_2.size() == 0)
    {
        return INFINITY;
    }
    if (sequence_1[0].size() != sequence_2[0].size())
    {
        throw invalid_argument("Sequences for evaluation have different element sizes");
    }
    // Safety checks
    if (!distance_fn_)
    {
        throw invalid_argument("DTW evaluator is not initialized with a cost function");
    }
    if (!initialized_ || sequence_1.size() >= x_dim_ || sequence_2.size() >= y_dim_)
    {
        cout << "Automatically resizing DTW matrix to fit arguments" << endl;
        SimpleDTW::Initialize(sequence_1.size(), sequence_2.size());
    }
    //Compute DTW cost for the two sequences
    for (unsigned int i = 1; i <= sequence_1.size(); i++)
    {
        for (unsigned int j = 1; j <= sequence_2.size(); j++)
        {
            double index_cost = distance_fn_(sequence_1[i - 1], sequence_2[j - 1]);
            double prev_cost = 0.0;
            // Get the three neighboring values from the matrix to use for the update
            double im1j = GetFromDTWMatrix(i - 1, j);
            double im1jm1 = GetFromDTWMatrix(i - 1, j - 1);
            double ijm1 = GetFromDTWMatrix(i, j - 1);
            // Start the update step
            if (im1j < im1jm1 && im1j < ijm1)
            {
                prev_cost = im1j;
            }
            else if (ijm1 < im1j && ijm1 < im1jm1)
            {
                prev_cost = ijm1;
            }
            else
            {
                prev_cost = im1jm1;
            }
            // Update the value in the matrix
            SetInDTWMatrix(i, j, index_cost + prev_cost);
        }
    }
    //Return total path cost
    return GetFromDTWMatrix(sequence_1.size(), sequence_2.size());
}
