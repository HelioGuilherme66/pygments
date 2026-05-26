*** Settings ***
Documentation     Simple example demonstrating syntax highlighting.
Test Setup        Keyword    argument    argument with ${VARIABLE}
Library           Process

*** Variables ***
${VARIABLE}       Variable value
@{LIST}           List    variable    here
&{DICT}           Key1=Value1    Key2=Value2

*** Test Cases ***
Keyword-driven example
    Initialize System
    Do Something
    Result Should Be    42
    [Teardown]    Cleanup System

Data-driven example
    [Template]    Keyword
    argument1    argument2
    argument    ${VARIABLE}
    @{LIST}

Gherkin
    Given system is initialized
    When something is done
    Then result should be "42"

| Pipes |
|  | [Documentation] | Also pipe separated format is supported. |
|  | Log | As this example demonstrates. |

*** Comments ***
This is a section of comments.
We can have many lines without any comment marker.

*** Keywords ***
Result Should Be
    [Arguments]    ${expected}
    [Tags]    whatever
    ${actual} =    Get Value    ${expected}
    Should be Equal    ${actual}    ${expected}

Then result should be "${expected}"
    Result Should Be    ${expected}

System is initialized
    # This is a single line comment
    Initialize System

something is done
    Do Something

Keyword
    [Arguments]    ${arg1}    ${arg2}    ${arg3}=${EMPTY}
    IF    "${arg1}" == "${arg2}"
        Log    Equal Arguments
    ELSE IF    "${arg1}" == "argument1"
        Log    arg1 is equal to argument1
    ELSE
        FOR    ${idx}    IN RANGE    4
            IF    ${idx} == 3    BREAK
            Log    ${\n}arg${idx+1} = ${arg${idx+1}}    console=True
        END
    END

Initialize System
    Log    System initialized

Do Something
    Run Keywords    Log    Done
    ...    AND    No Operation

Cleanup System
    TRY
        Log    %{HOME}
    EXCEPT
        Log To Console    \%{HOME} does not exist
    ELSE
        Log To Console    \%{HOME} exists
    END
    Log    System cleaned

Get Value
    [Arguments]    ${arg1}=42
    RETURN    ${arg1}
