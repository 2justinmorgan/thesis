
package main

import (
	"fmt"
	"testing"
	"github.com/google/go-cmp/cmp"
	"featuresgenerator/commons"
	"featuresgenerator/defines"
)

func TestGetSession(t *testing.T) {
	var testCases = []struct {
		inputDataFilePath string
		expectedSession defines.Session
	}{
		{
			"../data/raw_mouse_data/test_files/user7/session_0061629194",
			defines.Session{
				ID: "session_0061629194",
				User: "user7",
				InputDataFilePath: "../data/raw_mouse_data/test_files/user7/session_0061629194",
			},
		},
		{
			"training_files/user12/session_5265929106",
			defines.Session{
				ID: "session_5265929106",
				User: "user12",
				InputDataFilePath: "training_files/user12/session_5265929106",
			},
		},
	}

	for i, testCase := range testCases {
		testName := fmt.Sprintf("test%d",i);
		t.Run(testName, func(t *testing.T) {
			actualSession := commons.GetSession(testCase.inputDataFilePath)

			if !cmp.Equal(actualSession, testCase.expectedSession) {
				t.Errorf("\"%+v\" != \"%+v\"", actualSession, testCase.expectedSession);
			}
		})
	}
}
