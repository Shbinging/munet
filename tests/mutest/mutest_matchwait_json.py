"""Test match and wait send/expect-json step functionality."""
from munet.mutest.userapi import log
from munet.mutest.userapi import match_step_json
from munet.mutest.userapi import section
from munet.mutest.userapi import step_json
from munet.mutest.userapi import wait_step_json


js = step_json("r1", 'echo { "name": "chopps" }')
log("SIMPLE JSON: %s", js)

# expect passing tests

section("Test positive match_step_json calls")

match_step_json(
    "r1", 'echo \'{ "name": "chopps" }\'', '{ "name": "chopps"}', "Look for chopps"
)
wait_step_json(
    "r1",
    'echo \'{ "name": "chopps" }\'',
    '{ "name": "chopps"}',
    "Look for chopps",
    1,
    0.25,
)
wait_step_json(
    "r1",
    'echo \'{ "name": "chopps" }\'',
    '{ "name": "chopps"}',
    "Look for chopps",
    1,
    0.25,
    False,
)
wait_step_json(
    "r1",
    'echo \'{ "name": "chopps" }\'',
    '{ "name": "chopps"}',
    "Look for chopps",
    1,
    interval=0.25,
)
wait_step_json(
    "r1",
    'echo \'{ "name": "chopps" }\'',
    '{ "name": "chopps"}',
    "Look for chopps",
    1,
    interval=0.25,
    expect_fail=False,
)
wait_step_json(
    "r1",
    'echo \'{ "name": "chopps" }\'',
    '{ "name": "chopps"}',
    "Look for chopps",
    timeout=1,
    interval=0.25,
)
wait_step_json(
    "r1",
    'echo \'{ "name": "chopps" }\'',
    '{ "name": "chopps"}',
    "Look for chopps",
    timeout=1,
    interval=0.25,
    expect_fail=False,
)

section("Test negative (expect_fail) match_step_json calls")

match_step_json(
    "r1",
    """echo '{ "name": "other" }'""",
    '{ "name": "chopps"}',
    "Look for no chopps",
    True,
)
match_step_json(
    "r1",
    """echo '{ "name": "other" }'""",
    '{ "name": "chopps"}',
    "Look for no chopps",
    expect_fail=True,
)
wait_step_json(
    "r1",
    """echo '{ "name": "other" }'""",
    '{ "name": "chopps"}',
    "Look for no chopps",
    1,
    expect_fail=True,
)
wait_step_json(
    "r1",
    """echo '{ "name": "other" }'""",
    '{ "name": "chopps"}',
    "Look for no chopps",
    1,
    0.25,
    True,
)
wait_step_json(
    "r1",
    """echo '{ "name": "other" }'""",
    '{ "name": "chopps"}',
    "Look for no chopps",
    1,
    interval=0.25,
    expect_fail=True,
)
wait_step_json(
    "r1",
    """echo '{ "name": "other" }'""",
    '{ "name": "chopps"}',
    "Look for no chopps",
    timeout=1,
    expect_fail=True,
)
wait_step_json(
    "r1",
    """echo '{ "name": "other" }'""",
    '{ "name": "chopps"}',
    "Look for no chopps",
    timeout=1,
    interval=0.25,
    expect_fail=True,
)
wait_step_json(
    "r1", """echo 'not json'""", '{ "name": "other" }', "Look for chopps", 1, 0.25, True
)

section("Test json exact matching (exact_match == True)")

match_step_json(
    "r1",
    """echo '[{ "name": "other" }]'""",
    '[{ "name": "chopps"}]',
    "Look for no chopps",
    expect_fail=True,
    exact_match=True,
)
wait_step_json(
    "r1",
    """echo '[{ "name": "other" }]'""",
    '[{ "name": "chopps"}]',
    "Look for no chopps",
    1,
    expect_fail=True,
    exact_match=True,
)
match_step_json(
    "r1",
    """echo '[{ "name": "chopps" }]'""",
    '[{ "name": "chopps"}]',
    "Look for chopps",
    exact_match=True,
)
wait_step_json(
    "r1",
    """echo '[{ "name": "chopps" }]'""",
    '[{ "name": "chopps"}]',
    "Look for chopps",
    1,
    exact_match=True,
)

section("Test json matching rules (exact_match == False)")

json1 = '{"foo":"foo"}'
json2 = '{"foo":"foo", "bar":"bar"}'

_, ret = match_step_json(
    "r1",
    f"echo '{json2}'",
    json1,
    "Data within output object present",
)
test_step(
    ret == {'foo': 'foo', 'bar': 'bar'},
    "    Correct return value",
)
_, ret = match_step_json(
    "r1",
    f"echo '{json1}'",
    json2,
    "Data within output object not present",
    expect_fail=True,
)
test_step(
    ret == {'dictionary_item_removed': ["root['bar']"]},
    "    Correct return value",
)
# The return type should be a mix of dicts and lists. Not custom DeepDiff types!
test_step(
    type(ret['dictionary_item_removed']) is list,
    "    Correct return value type",
)

json1 = '[{"foo":"foo"}]'
json2 = '[{"foo":"foo"}, {"bar":"bar"}]'
json3 = '[{"bar":"bar"}, {"foo":"foo"}]'

_, ret = match_step_json(
    "r1",
    f"echo '{json2}'",
    json1,
    "Objects within output array present",
)
test_step(
    ret == [{'foo': 'foo'}, {'bar': 'bar'}],
    "    Correct return value",
)
_, ret = match_step_json(
    "r1",
    f"echo '{json1}'",
    json2,
    "Objects within output array not present",
    expect_fail=True,
)
test_step(
    ret == {'iterable_item_removed': {'root[1]': {'bar': 'bar'}}},
    "    Correct return value",
)
_, ret = match_step_json(
    "r1",
    f"echo '{json2}'",
    json3,
    "Both objects within output array present",
)
test_step(
    ret == [{'foo': 'foo'}, {'bar': 'bar'}],
    "    Correct return value",
)

json1 = '["foo"]'
json2 = '["foo", "bar"]'
json3 = '["bar", "foo"]'

_, ret = match_step_json(
    "r1",
    f"echo '{json2}'",
    json1,
    "Data in different arrays don't match",
    expect_fail=True,
)
test_step(
    ret == {'iterable_item_added': {'root[1]': 'bar'}},
    "    Correct return value",
)
_, ret = match_step_json(
    "r1",
    f"echo '{json1}'",
    json2,
    "Data in different arrays don't match",
    expect_fail=True,
)
test_step(
    ret == {'iterable_item_removed': {'root[1]': 'bar'}},
    "    Correct return value",
)
_, ret = match_step_json(
    "r1",
    f"echo '{json2}'",
    json3,
    "Data in equivalent arrays match"
)
test_step(
    ret == ['foo', 'bar'],
    "    Correct return value",
)

json1 = '{"level1": ["level2", {"level3": ["level4"]}]}'
json2 = '{"level1": ["level2", {"level3": ["level4"], "l3": "l4"}]}'
json3 = '{"level1": ["level2", {"level3": ["level4", {"level5": "l6"}]}]}'
json4 = '{"level1": ["level2", {"level3": ["level4", "l4"]}]}'

_, ret = match_step_json(
    "r1",
    f"echo '{json2}'",
    json1,
    "Data within output object present (nested)",
)
test_step(
    ret == {'level1': ['level2', {'level3': ['level4'], 'l3': 'l4'}]},
    "    Correct return value",
)
_, ret = match_step_json(
    "r1",
    f"echo '{json3}'",
    json1,
    "Objects within output array present (nested)",
)
test_step(
    ret == {'level1': ['level2', {'level3': ['level4', {'level5': 'l6'}]}]},
    "    Correct return value",
)
_, ret = match_step_json(
    "r1",
    f"echo '{json4}'",
    json1,
    "Data in different arrays don't match (nested)",
    expect_fail=True
)
test_step(
    ret == {'iterable_item_added': {"root['level1'][1]['level3'][1]": 'l4'}},
    "    Correct return value",
)
match_step_json(
    "r1",
    """echo '{}'""",
    '{ "name": "chopps"}',
    "empty json output doesn't match",
    expect_fail=True,
    exact_match=False,
)
