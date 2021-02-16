
package commons

import (
	"fmt"
	"os"
	"io"
	"bytes"
	"strings"
	"featuresgenerator/defines"
)

// GetSession returns the Session pertaining to the passed-in session data input file
func GetSession(inputDataFilePath string) defines.Session {
	filePathTokens := strings.Split(inputDataFilePath, "/")

	sessionID := ""
	user := ""

	for _, token := range filePathTokens {
		if strings.Contains(token, "user") {
			user = token
		}
		if strings.Contains(token, "session_") {
			sessionID = token
		}
	}

	if len(sessionID) <= 0 || len(user) <= 0 {
		fmt.Fprintf(os.Stderr, "unable to get session info\n")
		os.Exit(1)
	}

	numLines := FileLinesCounter(SafeOpen(inputDataFilePath))

	return defines.Session{
		ID: sessionID,
		User: user,
		InputDataFilePath: inputDataFilePath,
		Features: InitializeFeaturesMap(numLines),
	}
}

// InitializeFeaturesMap returns the hashmap containing all features, with preallocated records slices
func InitializeFeaturesMap(numRecords int) map[string]defines.Feature {
    featuresMap := make(map[string]defines.Feature)

    for _,featureName := range defines.GetFeaturesNames() {
        intNum := int(0)
        featuresMap[featureName] = defines.Feature{
            Name: featureName,
            Records: make([]float64, numRecords),
            RecordsCounter: &intNum,
            NumRecords: numRecords,
        }
    }

    return featuresMap
}

// FileLinesCounter returns the number of lines in a file
func FileLinesCounter(file *os.File) int {
    buf := make([]byte, 32*1024)
    count := 0
    lineSep := []byte{'\n'}

    for {
        c, err := file.Read(buf)
        count += bytes.Count(buf[:c], lineSep)

        switch {
            case err == io.EOF:
                file.Seek(0, io.SeekStart)
                return count

            case err != nil:
                fmt.Fprintf(os.Stderr, "error counting lines in file\n")
                os.Exit(1)
        }
    }
}

// SafeOpen returns a file pointer, via os.Open, or exits program upon open error
func SafeOpen(filePath string) *os.File {
    file, err := os.Open(filePath)
    if err != nil {
        fmt.Fprintf(os.Stderr, "error opening file \"%s\"", filePath)
        os.Exit(1)
    }
    return file
}

// OutputSlice writes a float64 slice to the inputted file path
func OutputSlice(filePath string, floatNums []float64) {
    f, err := os.Create(filePath)
    if err != nil {
        fmt.Fprintf(os.Stderr, "error writing slice to file path \"%s\"\n", filePath)
    }
    defer f.Close()

    l := len(floatNums)
    fmt.Fprintf(f, "[%f", floatNums[0])
    for i := 1; i<l; i++ {
       fmt.Fprintf(f, ",%f", floatNums[i])  // print values to f, one per line
    }
    fmt.Fprintf(f, "]\n")
}
