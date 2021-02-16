
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
		numLines int
		expectedSession defines.Session
	}{
		{
			"../data/raw_mouse_data/test_files/user7/session_0061629194",
			2,
			defines.Session{
				ID: "session_0061629194",
				User: "user7",
				InputDataFilePath: "../data/raw_mouse_data/test_files/user7/session_0061629194",
				Features: commons.InitializeFeaturesMap(2),
			},
		},
		{
			"training_files/user12/session_5265929106",
			3,
			defines.Session{
				ID: "session_5265929106",
				User: "user12",
				InputDataFilePath: "training_files/user12/session_5265929106",
				Features: commons.InitializeFeaturesMap(3),
			},
		},
	}

	for i, testCase := range testCases {
		testName := fmt.Sprintf("test%d",i);
		t.Run(testName, func(t *testing.T) {
			actualSession := commons.GetSession(testCase.inputDataFilePath, testCase.numLines)

			if !cmp.Equal(actualSession.ID, testCase.expectedSession.ID) {
				t.Errorf("\"%+v\" != \"%+v\"", actualSession.ID, testCase.expectedSession.ID);
			}
            if !cmp.Equal(actualSession.User, testCase.expectedSession.User) {
                t.Errorf("\"%+v\" != \"%+v\"", actualSession.User, testCase.expectedSession.User);
            }
            if !cmp.Equal(actualSession.InputDataFilePath, testCase.expectedSession.InputDataFilePath) {
                t.Errorf("\"%+v\" != \"%+v\"", actualSession.InputDataFilePath, testCase.expectedSession.InputDataFilePath);
            }
            if !cmp.Equal(actualSession.Features, testCase.expectedSession.Features) {
                t.Errorf("\"%+v\" != \"%+v\"", actualSession.Features, testCase.expectedSession.Features);
            }
		})
	}
}
