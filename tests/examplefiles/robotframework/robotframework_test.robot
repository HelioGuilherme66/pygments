*** Settings ***
Documentation    Simple example demonstrating syntax highlighting.
Library          Process
Test Setup       Keyword    argument   argument with ${VARIABLE}

*** Variables ***
${VARIABLE}      Variable value
@{LIST}          List    variable    here
&{DICT}          Key1=Value1    Key2=Value2

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

*** Keywords ***
Result Should Be
    [Arguments]    ${expected}
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
    [Arguments]    ${arg1}    ${arg2}   ${arg3}=${EMPTY}
    IF    "${arg1}" == "${arg2}"
        Log     Equal Arguments
    ELSE IF    "${arg1}" == "argument1"
        Log     arg1 is equal to argument1
    ELSE
        FOR    ${idx}    IN RANGE    3
            Log    ${\n}arg${idx+1} = ${arg${idx+1}}    console=True
        END
    END

Initialize System
    Log    System initialized

Do Something
    Log    Done

Cleanup System
    Log    System cleaned

Get Value
    [Arguments]    ${arg1}=42
    RETURN    ${arg1}

