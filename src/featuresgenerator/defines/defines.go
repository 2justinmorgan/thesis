package defines

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

// Session pertains to the passed-in session mouse data input file
type Session struct {
	ID string
	User string
	InputDataFilePath string
	Features map[string]Feature
}

// Feature contains the info of a specific feature, i.e. velocity or jerk
type Feature struct {
	Name string
	Records []int
	RecordsCounter int
}
