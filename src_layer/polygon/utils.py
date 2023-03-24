from collections import namedtuple


Problem = namedtuple(
    "Problem",
    [
        "id",
        "owner",
        "name",
        "deleted",
        "favourite",
        "accessType",
        "revision",
        "latestPackage",
        "modified",
        "letter",
    ],
)


ProblemInfo = namedtuple(
    "ProblemInfo",
    ["timeLimit", "inputFile", "outputFile", "interactive", "memoryLimit"],
)

Statement = namedtuple(
    "Statement",
    ["encoding", "name", "legend", "input", "output", "scoring", "notes", "tutorial"],
)

ResourceAdvancedProperties = namedtuple(
    "ResourceAdvancedProperties", ["forTypes", "main", "stages", "assets"]
)

File = namedtuple(
    "File",
    [
        "name",
        "modificationTimeSeconds",
        "length",
        "sourceType",
        "resourceAdvancedProperties",
    ],
)

Solution = namedtuple(
    "Solution", ["name", "modificationTimeSeconds", "length", "source_type", "tag"]
)

Test = namedtuple(
    "Test",
    [
        "index",
        "useInStatements",
        "manual",
        "scriptLine",
        "groups",
        "points",
        "inputForStatement",
        "outputForStatement",
        "verifyInputOutputForStatements",
    ],
)

Package = namedtuple(
    "Package", ["id", "revision", "creationTimeSeconds", "state", "comment", "type"]
)

TestGroup = namedtuple(
    "TestGroupObject", ["name", "pointsPolicy", "feedbackPolicy", "dependencies"]
)
