from collections import namedtuple

Problem = (namedtuple('Problem', ['Id', 'Owner', 'Name', 'Deleted', 'Favourite',
    'AccessType', 'Revision', 'LatestPackage', 'Modified']))

ProblemInfo = namedtuple('ProblemInfo', ['InputFile', 'OutputFile', 'Interactive', 'TimeLimit', 'MemoryLimit'])

Statement = namedtuple('Statement', ['Encoding', 'Name', 'Legend', 'Input', 'Output', 'Scoring', 'Notes', 'Tutorial'])

ResourceAdvancedProperties = namedtuple('ResourceAdvancedProperties', ['ForTypes', 'Main', 'Stages', 'Assets'])

File = namedtuple('File', ['Name', 'ModificationTimeSeconds', 'Length', 'SourceType', 'ResourceAdvancedProperties'])

Solution = namedtuple('Solution', ['name', 'modification_time_seconds', 'length', 'source_type', 'tag'])

Test = namedtuple('Test', ['index manual input description use_in_statements script_line groups points input_for_statement output_for_statement verify_input_output_for_statements'])