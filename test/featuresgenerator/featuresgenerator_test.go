package main

import (
	"fmt"
	"os"
	"testing"
	"io/ioutil"
)

func createTempFile(content []byte) (filePath string) {
	tmpFile, err := ioutil.TempFile(os.TempDir(), "temp_file")

	_, err = tmpFile.Write(content)

	err = tmpFile.Close()

	if err != nil {
		fmt.Fprintf(os.Stderr, "error creating temp file\n%s\n", err)
	}

	return tmpFile.Name()
}

func TestTempFile(t *testing.T) {
	var testCases = []struct {
		fileContent []byte
	}{
		{[]byte("this is sample file content")},
	}

	for i, testCase := range testCases {
		testName := fmt.Sprintf("test%d",i);
		t.Run(testName, func(t *testing.T) {
			tmpFilePath := createTempFile(testCase.fileContent)

			actualContent, err := ioutil.ReadFile(tmpFilePath)
			if err != nil { fmt.Fprintf(os.Stderr, "unable to read file content\n%s\n", err) }

			err = os.Remove(tmpFilePath)
			if err != nil { fmt.Fprintf(os.Stderr, "unable to remove a file\n%s\n", err) }

			if  string(actualContent) != string(testCase.fileContent) {
				t.Errorf("\"%s\" != \"%s\"", actualContent, testCase.fileContent);
			}
		})
	}
}

func TestCheckArgsReturnsPassedInArgvFilePath(t *testing.T) {
	t.Run("test1", func(t *testing.T) {
		tmpFilePath := createTempFile([]byte("this is random file content"))

		argv := []string{"./program_binary_name", tmpFilePath}

		checkArgsFilePath := checkArgs(len(argv), argv)

		if checkArgsFilePath != tmpFilePath {
			t.Errorf("\"%s\" != \"%s\"", checkArgsFilePath, tmpFilePath)
		}
	})
}
