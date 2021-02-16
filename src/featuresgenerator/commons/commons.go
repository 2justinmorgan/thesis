
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

	inputDataFile := SafeOpen(inputDataFilePath)
	numLines := FileLinesCounter(inputDataFile)

	return defines.Session{
		ID: sessionID,
		User: user,
		InputDataFile: inputDataFile,
		Features: InitializeFeaturesMap(numLines),
	}
}

// InitializeFeaturesMap returns the hashmap containing all features, with preallocated records slices
func InitializeFeaturesMap(numRecords int) map[string]defines.Feature {
    featuresMap := make(map[string]defines.Feature)

    for _,featureName := range defines.GetFeaturesNames() {
        featuresMap[featureName] = defines.Feature{
            Name: featureName,
            Records: make([]float64, numRecords),
            RecordsCounter: 0,
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
