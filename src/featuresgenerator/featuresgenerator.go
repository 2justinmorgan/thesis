
package main

import (
	"fmt"
	"os"
	"path/filepath"
	"featuresgenerator/commons"
	"featuresgenerator/generator"
)

func printUsage() {
	fmt.Fprintf(os.Stderr, "Usage: ./%s <mouse_data_csv>\n", filepath.Base(os.Args[0]))
}

func checkArgs(argc int, argv []string) string {
	if argc != 2 {
		printUsage()
		os.Exit(1)
	}

	var intputFilePath string = argv[1]

	if _, err := os.Stat(intputFilePath); os.IsNotExist(err) {
		fmt.Fprintf(os.Stderr, "%s file not found\n%s\n", intputFilePath, err)
		os.Exit(1)
	}

	return intputFilePath
}

func main() {
	inputFilePath := checkArgs(len(os.Args), os.Args)

	session := commons.GetSession(inputFilePath, commons.FileLinesCounter(inputFilePath))

	generator.OutputAllFeatures(session)
}
