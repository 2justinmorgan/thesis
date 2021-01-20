
package commons

import (
	"fmt"
	"os"
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

	return defines.Session{
		ID: sessionID,
		User: user,
		InputDataFilePath: inputDataFilePath,
	}
}
