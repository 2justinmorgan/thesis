
package defines

import (
    "os"
)

// GetFeaturesNames returns a str slice of the features to be generated
func GetFeaturesNames() (features []string) {
	return []string{
		"velocity",
		"xvelocity",
		"yvelocity",
		"acceleration",
		"jerk",
		"theta",
	}
}

// Point contains (x, y) coordinates, and is used as the base composition of a TPoint
type Point struct {
	X int
	Y int
}

// TPoint is a Point with a time attribute
type TPoint struct {
	Point
	Time float64
}

// Session pertains to the passed-in session mouse data input file
type Session struct {
	ID string
	User string
	InputDataFile *os.File
	Features map[string]Feature
}

// Feature contains the info of a specific feature, i.e. velocity or jerk
type Feature struct {
	Name string
	Records []float64
	RecordsCounter int
}
