import { useState } from "react";
import {
  Alert,
  Pressable,
  StyleSheet,
  Text,
  View,
} from "react-native";
import { useRouter } from "expo-router";
import { loginByNumber, Employee } from "../lib/api";

export default function LoginScreen() {
  const [number, setNumber] = useState("");
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handlePress = (digit: string) => {
    if (number.length < 10) {
      setNumber((prev) => prev + digit);
    }
  };

  const handleClear = () => setNumber("");

  const handleEnter = async () => {
    if (!number) return;
    setLoading(true);
    try {
      const employee = await loginByNumber(number);
      router.push({
        pathname: "/punch",
        params: { employee: JSON.stringify(employee) },
      });
    } catch (e: any) {
      Alert.alert("Error", e.message || "Employee not found");
    } finally {
      setLoading(false);
    }
  };

  const numpadKeys = [
    ["7", "8", "9"],
    ["4", "5", "6"],
    ["1", "2", "3"],
    ["0", null, "Clear"],
  ];

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Enter Number or Scan Badge</Text>

      <View style={styles.display}>
        <Text style={styles.displayText}>{number || " "}</Text>
      </View>

      <View style={styles.numpad}>
        {numpadKeys.map((row, rowIndex) => (
          <View key={rowIndex} style={styles.row}>
            {row.map((key, keyIndex) => {
              if (key === null) {
                return <View key={keyIndex} style={styles.keyEmpty} />;
              }
              if (key === "Clear") {
                return (
                  <Pressable
                    key={keyIndex}
                    style={({ pressed }) => [
                      styles.key,
                      styles.keyClear,
                      pressed && styles.keyPressed,
                    ]}
                    onPress={handleClear}
                  >
                    <Text style={styles.keyText}>Clear</Text>
                  </Pressable>
                );
              }
              return (
                <Pressable
                  key={keyIndex}
                  style={({ pressed }) => [
                    styles.key,
                    pressed && styles.keyPressed,
                  ]}
                  onPress={() => handlePress(key)}
                >
                  <Text style={styles.keyText}>{key}</Text>
                </Pressable>
              );
            })}
          </View>
        ))}
      </View>

      <Pressable
        style={({ pressed }) => [
          styles.enterButton,
          (loading || !number) && styles.enterButtonDisabled,
          pressed && styles.keyPressed,
        ]}
        onPress={handleEnter}
        disabled={loading || !number}
      >
        <Text style={styles.enterText}>
          {loading ? "Loading..." : "Enter"}
        </Text>
      </Pressable>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fff",
    alignItems: "center",
    justifyContent: "center",
    padding: 20,
  },
  title: {
    fontSize: 24,
    fontWeight: "bold",
    marginBottom: 20,
    color: "#000",
  },
  display: {
    width: "80%",
    backgroundColor: "#f0f0f0",
    borderRadius: 8,
    padding: 16,
    marginBottom: 20,
    alignItems: "center",
    borderWidth: 1,
    borderColor: "#ccc",
  },
  displayText: {
    fontSize: 32,
    fontWeight: "bold",
    color: "#000",
    letterSpacing: 4,
  },
  numpad: {
    width: "80%",
    borderWidth: 1,
    borderColor: "#ccc",
    backgroundColor: "#f5f5f5",
    padding: 4,
  },
  row: {
    flexDirection: "row",
    justifyContent: "center",
  },
  key: {
    flex: 1,
    margin: 4,
    paddingVertical: 18,
    backgroundColor: "#e8e8e8",
    alignItems: "center",
    justifyContent: "center",
    borderWidth: 1,
    borderColor: "#ccc",
  },
  keyClear: {
    flex: 2,
  },
  keyEmpty: {
    flex: 1,
    margin: 4,
  },
  keyText: {
    fontSize: 28,
    fontWeight: "bold",
    color: "#000",
  },
  enterButton: {
    marginTop: 24,
    width: "70%",
    paddingVertical: 18,
    backgroundColor: "#fff",
    borderWidth: 3,
    borderColor: "#2e8b57",
    borderRadius: 8,
    alignItems: "center",
  },
  enterButtonDisabled: {
    opacity: 0.5,
  },
  keyPressed: {
    opacity: 0.6,
  },
  enterText: {
    fontSize: 32,
    fontWeight: "bold",
    color: "#000",
  },
});
