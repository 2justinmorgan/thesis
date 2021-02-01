
package generator

import (
	"fmt"
	"os"
	"math"
	"strings"
	"strconv"
	"featuresgenerator/defines"
)

// GetTPoint returns the (x, y, time) values of a single line of the input csv file
func GetTPoint(csvLine string) defines.TPoint {
	// description: record timestamp,client timestamp,button,state,x,y
	// input (str):
	// 291.082999945,291.082,NoButton,Move,544,594
	// output (TPoint):
	// TPoint(544, 594, 291.082)

	csvLineList := strings.Split(csvLine, ",")
	x, err := strconv.Atoi(csvLineList[4])
	y, err := strconv.Atoi(csvLineList[5])
	time, err := strconv.ParseFloat(csvLineList[1], 64)

	if err != nil { 
		fmt.Fprintf(os.Stderr, "%s\n", err)
		os.Exit(1)
	}

    return defines.TPoint{Point: defines.Point{X: x, Y: y}, Time: time}
}

// GetTheta returns the angle traversed from pointA to pointB
func GetTheta(pointA defines.Point, pointB defines.Point) (theta float64) {
	deltaX := math.Abs(float64(pointA.X - pointB.X))
	deltaY := math.Abs(float64(pointA.Y - pointB.Y))
    return math.Atan2(deltaY, deltaX)
}

// GetVelocity returns the angular, vertical, or horizontal velocity of two tpoints
func GetVelocity(axis string, tpointA defines.TPoint, tpointB defines.TPoint) (velocity float64) {
	if axis != "x" && axis != "y" && axis != "xy" {
		return -1
	}

	if axis == "xy" {
		Xvelocity := GetVelocity("x", tpointA, tpointB)
		Yvelocity := GetVelocity("y", tpointA, tpointB)
		return math.Pow(math.Pow(Xvelocity, 2) + math.Pow(Yvelocity, 2), .5)
	}

	deltaAxis := 0.0

	if axis == "x" {
		deltaAxis = math.Abs(float64(tpointA.X - tpointB.X))
	}
	if axis == "y" {
		deltaAxis = math.Abs(float64(tpointA.Y - tpointB.Y))
	}

	deltaT := math.Abs(tpointA.Time - tpointB.Time)

	if deltaT == 0 { return 0.0 }

	return deltaAxis / deltaT
}

// GetFeatureVal is a wrapper func for all features calculations
func GetFeatureVal(featureName string, tpoints []defines.TPoint) (featureVal float64) {
	//
	// need case that returns if feature_name is invalid
	//
    if strings.Contains(featureName, "velocity") {
        if featureName == "velocity" {
			return GetVelocity("xy", tpoints[0], tpoints[1])
		}
        // the first arg, axis, can be 'x' or 'y'
		return GetVelocity(string(featureName[0]), tpoints[0], tpoints[1])
	}

    if featureName == "acceleration" {
        velocityA := GetVelocity("xy", tpoints[0], tpoints[1])
        velocityB := GetVelocity("xy", tpoints[2], tpoints[3])
		deltaT := math.Abs(tpoints[0].Time - tpoints[3].Time)
		if deltaT == 0 { return 0 }
		return math.Abs(velocityA - velocityB) / deltaT
	}

    if featureName == "jerk" {
        accelerationA := GetFeatureVal("acceleration", tpoints[:4])
        accelerationB := GetFeatureVal("acceleration", tpoints[4:])
		deltaT := math.Abs(tpoints[0].Time - tpoints[7].Time)
		if deltaT == 0 { return 0 }
		return math.Abs(accelerationA - accelerationB) / deltaT
	}

    if featureName == "theta" {
		pointA := defines.Point{X: tpoints[0].X, Y: tpoints[0].Y} 
		pointB := defines.Point{X: tpoints[1].X, Y: tpoints[1].Y}
		return GetTheta(pointA, pointB)
	}

	return -1
}