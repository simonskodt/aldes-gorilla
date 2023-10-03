truth_filename = "data/HbB_FASTAs-out.txt"  # replace with your file path
test_filename = "data/HbB_FASTAs-test-out.txt"

entries_truth = {}
entries_test = {}
def loadEntries(dict, filename):
    with open(filename, "r") as f:
        while True:
            line1 = f.readline().strip()
            if not line1:
                break  # end of file
            line2 = f.readline().strip()
            line3 = f.readline().strip()
            x, num = line1.split()
            entry = {
                "num": int(num),
                "string1": line2,
                "string2": line3,
            }
            dict[x] = entry
loadEntries(entries_truth, truth_filename)
loadEntries(entries_test, test_filename)

print("Is the length the same? " + str(len(entries_test) == len(entries_truth)))

# Compare values
for key in set(entries_truth.keys()):
    if(key in entries_test):
        if entries_truth[key] != entries_test[key]:
            truthEntry = entries_truth[key]
            testEntry = entries_test[key]
            if(truthEntry["num"] != testEntry["num"]):
                print("Num is not the same for entry " + key + ". Truth: " + truthEntry["num"] + "; Test: " + testEntry["num"])
            if(truthEntry["string1"] != testEntry["string1"]):
                print("String1 is not the same for entry " + key)
                print("Truth: " + truthEntry["string1"])
                print("Test: " + testEntry["string1"])
            if(truthEntry["string2"] != testEntry["string2"]):
                print("String2 is not the same for entry " + key)
                print("Truth: " + truthEntry["string2"])
                print("Test: " + testEntry["string2"])
    else:
        splittedKey = key[:-1].split("--")
        reversedKey = splittedKey[1] + "--" + splittedKey[0] + ":"
        if(reversedKey in entries_test):
            truthEntry = entries_truth[key]
            testEntry = entries_test[reversedKey]
            if(truthEntry["num"] != testEntry["num"]):
                print("Num is not the same for entry " + key + ". Truth: " + truthEntry["num"] + "; Test: " + testEntry["num"])
            if(truthEntry["string1"] != testEntry["string2"]):
                print("rString1 is not the same for entry " + key)
                print("Truth: " + truthEntry["string1"])
                print("Test: " + testEntry["string1"])
            if(truthEntry["string2"] != testEntry["string1"]):
                print("rString2 is not the same for entry " + key)
                print("Truth: " + truthEntry["string2"])
                print("Test: " + testEntry["string2"])
        else:
            print("Missing " + key + " in test set")
