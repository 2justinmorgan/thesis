
package main

import (
	"fmt"
	"testing"
	"math"
	"featuresgenerator/defines"
	"featuresgenerator/generator"
)

func floatEqual(a float64, b float64) (isEqual bool) {
	if math.Abs(a - b) > 1e-6 {
		return false
	}
	return true
}

func TestGetTheta(t *testing.T) {
	var testCases = []struct {
		pointA defines.Point
		pointB defines.Point
		expectedTheta float64
	}{
		{
			defines.Point{X: 23, Y: 42},
			defines.Point{X: 31, Y: 45},
			0.35877067027057225,
		},
		{
			defines.Point{X: 1020, Y: 355},
			defines.Point{X: 1003, Y: 361},
			0.3392926144540447,
		},
	}

	for i, testCase := range testCases {
		testName := fmt.Sprintf("test%d",i);
		t.Run(testName, func(t *testing.T) {
			actualTheta := generator.GetTheta(testCase.pointA, testCase.pointB)

			if !floatEqual(actualTheta, testCase.expectedTheta) {
				t.Errorf("\"%f\" != \"%f\"", actualTheta, testCase.expectedTheta);
			}
		})
	}
}

func TestGetVelocity(t *testing.T) {
	type Point = defines.Point
	type TPoint = defines.TPoint

	var testCases = []struct {
		axis string
		tpointA TPoint
		tpointB TPoint
		expectedVelocity float64
	}{
		{"v", TPoint{Point: Point{X: 1, Y: 2}, Time: 1}, TPoint{Point: Point{X: 1, Y: 2}, Time: 1}, -1},
		{"", TPoint{Point: Point{X: 13, Y: 52}, Time: 7}, TPoint{Point: Point{X: 18, Y: 44}, Time: 9}, -1},
		{"x", TPoint{Point: Point{X: 0, Y: 0}, Time: 0}, TPoint{Point: Point{X: 1, Y: 0}, Time: 1}, 1},
		{"x", TPoint{Point: Point{X: 10, Y: 20}, Time: 5}, TPoint{Point: Point{X: 15, Y: 30}, Time: 5}, 0},
		{"x", TPoint{Point: Point{X: 487, Y: 912}, Time: 3419.371}, TPoint{Point: Point{X: 488, Y: 915}, Time: 3419.62}, 4.016064257},
		{"x", TPoint{Point: Point{X: 50, Y: 75}, Time: 0.001}, TPoint{Point: Point{X: 55, Y: 76}, Time: 0.092}, 54.94505495},
		{"y", TPoint{Point: Point{X: 0, Y: 2}, Time: 0}, TPoint{Point: Point{X: 1, Y: 4}, Time: 1}, 2},
		{"x", TPoint{Point: Point{X: 100, Y: 200}, Time: 50}, TPoint{Point: Point{X: 150, Y: 300}, Time: 50}, 0},
		{"y", TPoint{Point: Point{X: 985, Y: 102}, Time: 40.95}, TPoint{Point: Point{X: 993, Y: 94}, Time: 41}, 160},
		{"y", TPoint{Point: Point{X: 0, Y: 4}, Time: 0.00005}, TPoint{Point: Point{X: 3, Y: 2}, Time: 0.0038}, 533.333333333},
		{"yx", TPoint{Point: Point{X: 34, Y: 99}, Time: 54}, TPoint{Point: Point{X: 23, Y: 103}, Time: 55}, -1},
		{"xy", TPoint{Point: Point{X: 10, Y: 20}, Time: 1}, TPoint{Point: Point{X: 15, Y: 32}, Time: 2}, 13},
		{"xy", TPoint{Point: Point{X: 31, Y: 52}, Time: 30.35}, TPoint{Point: Point{X: 15, Y: 32}, Time: 30.35}, 0},
		{"xy", TPoint{Point: Point{X: 56, Y: 341}, Time: 15290.04}, TPoint{Point: Point{X: 57, Y: 341}, Time: 15290.29}, 4.0},
		{"xy", TPoint{Point: Point{X: 1490, Y: 888}, Time: 0.92}, TPoint{Point: Point{X: 1539, Y: 831}, Time: 1.005}, 884.3115516689962},
	}

	for i, testCase := range testCases {
		testName := fmt.Sprintf("test%d",i);
		t.Run(testName, func(t *testing.T) {
			actualVelocity := generator.GetVelocity(testCase.axis, testCase.tpointA, testCase.tpointB)

			if !floatEqual(actualVelocity, testCase.expectedVelocity) {
				t.Errorf("\"%f\" != \"%f\"", actualVelocity, testCase.expectedVelocity);
			}
		})
	}
}

func TestGetFeatureVal(t *testing.T) {
	type Point = defines.Point
	type TPoint = defines.TPoint

	var testCases = []struct{
		featureName string
		tpoints []TPoint
		expectedFeatureVal float64
	}{
        {
            "theta",
            []TPoint{
				TPoint{Point: Point{X: 25, Y: 12}, Time: 0.33},
				TPoint{Point: Point{X: 18, Y: 33}, Time: 1.4},
			}, 
			1.2490457723982544,
		},
        {
            "theta",
            []TPoint{
				TPoint{Point: Point{X: 556, Y: 273}, Time: 8.33927},
				TPoint{Point: Point{X: 556, Y: 255}, Time: 8.4599},
			},
			1.5707963267948966,
		},
        {
            "velocity",
            []TPoint{
				TPoint{Point: Point{X: 34, Y: 55}, Time: 0.334},
				TPoint{Point: Point{X: 33, Y: 52}, Time: 0.397},
			},
			50.19488349473618,
		},
        {
            "xvelocity",
            []TPoint{
				TPoint{Point: Point{X: 34, Y: 55}, Time: 0.334},
				TPoint{Point: Point{X: 33, Y: 52}, Time: 0.397},
			},
			15.873015873,
		},
        {
            "yvelocity",
            []TPoint{
				TPoint{Point: Point{X: 34, Y: 55}, Time: 0.334},
				TPoint{Point: Point{X: 33, Y: 52}, Time: 0.397},
			},
			47.619047619,
		},
        {
            "acceleration",
            []TPoint{
				TPoint{Point: Point{X: 2, Y: 4}, Time: 1},
				TPoint{Point: Point{X: 1, Y: 3}, Time: 2},
				TPoint{Point: Point{X: 2, Y: 3}, Time: 4},
				TPoint{Point: Point{X: 4, Y: 8}, Time: 8},
			},
			0.009703194369924173,
		},
        {
            "acceleration",
            []TPoint{
				TPoint{Point: Point{X: 2, Y: 4}, Time: 1},
				TPoint{Point: Point{X: 1, Y: 3}, Time: 1},
				TPoint{Point: Point{X: 2, Y: 3}, Time: 1},
				TPoint{Point: Point{X: 4, Y: 8}, Time: 1},
			},
			0,
		},
        {
            "jerk",
            []TPoint{
				TPoint{Point: Point{X: 3, Y: 6}, Time: 0.1},
				TPoint{Point: Point{X: 2, Y: 4}, Time: 0.3},
				TPoint{Point: Point{X: 1, Y: 3}, Time: 0.6},
				TPoint{Point: Point{X: 5, Y: 4}, Time: 1},
				TPoint{Point: Point{X: 6, Y: 7}, Time: 1.1},
				TPoint{Point: Point{X: 8, Y: 5}, Time: 1.4},
				TPoint{Point: Point{X: 5, Y: 4}, Time: 1.6},
				TPoint{Point: Point{X: 2, Y: 2}, Time: 1.9},
			},
			1.2602714455166364,
		},
        {
            "jerk",
            []TPoint{
				TPoint{Point: Point{X: 344, Y: 108}, Time: 0.99371},
				TPoint{Point: Point{X: 345, Y: 101}, Time: 0.99914},
				TPoint{Point: Point{X: 347, Y: 93}, Time: 1.0038},
				TPoint{Point: Point{X: 353, Y: 90}, Time: 1.02388},
				TPoint{Point: Point{X: 355, Y: 90}, Time: 1.13884},
				TPoint{Point: Point{X: 355, Y: 94}, Time: 1.177483},
				TPoint{Point: Point{X: 357, Y: 95}, Time: 1.201},
				TPoint{Point: Point{X: 358, Y: 98}, Time: 1.237114},
			},
			131170.79429774,
		},
        {
            "jerk",
            []TPoint{
				TPoint{Point: Point{X: 3, Y: 6}, Time: 0.1},
				TPoint{Point: Point{X: 2, Y: 4}, Time: 0.1},
				TPoint{Point: Point{X: 1, Y: 3}, Time: 0.1},
				TPoint{Point: Point{X: 5, Y: 4}, Time: .1},
				TPoint{Point: Point{X: 6, Y: 7}, Time: .1},
				TPoint{Point: Point{X: 8, Y: 5}, Time: .1},
				TPoint{Point: Point{X: 5, Y: 4}, Time: .1},
				TPoint{Point: Point{X: 2, Y: 2}, Time: .1},
			},
			0,
		},
	}

	for i, testCase := range testCases {
		testName := fmt.Sprintf("test%d",i);
		t.Run(testName, func(t *testing.T) {
			actualFeatureVal := generator.GetFeatureVal(testCase.featureName, testCase.tpoints)

			if !floatEqual(actualFeatureVal, testCase.expectedFeatureVal) {
				t.Errorf("\"%f\" != \"%f\"", actualFeatureVal, testCase.expectedFeatureVal);
			}
		})
	}
}
