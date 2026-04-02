import { useCallback, useEffect, useState } from "react";
import {
  Alert,
  ScrollView,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from "react-native";
import { useLocalSearchParams, useRouter } from "expo-router";
import {
  Employee,
  PunchRecord,
  punchIn,
  punchOut,
  getTodayPunches,
  getCurrentStatus,
} from "../lib/api";

const DAYS = [
  "sunday",
  "monday",
  "tuesday",
  "wednesday",
  "thursday",
  "friday",
  "saturday",
];
const DAY_LABELS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];

function formatDate(d: Date): string {
  return d.toLocaleDateString("en-US", {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
  });
}

function formatTime(iso: string): string {
  const d = new Date(iso);
  return d.toLocaleTimeString("en-US", {
    hour: "numeric",
    minute: "2-digit",
    hour12: true,
  });
}

function formatScanDate(dateStr: string): string {
  const [y, m, d] = dateStr.split("-");
  return `${parseInt(m)}/${parseInt(d)}/${y}`;
}

export default function PunchScreen() {
  const { employee: employeeJson } = useLocalSearchParams<{ employee: string }>();
  const router = useRouter();
  const employee: Employee = JSON.parse(employeeJson || "{}");

  const [todayPunches, setTodayPunches] = useState<PunchRecord[]>([]);
  const [isPunchedIn, setIsPunchedIn] = useState(false);
  const [loading, setLoading] = useState(false);

  const loadData = useCallback(async () => {
    try {
      const [punches, status] = await Promise.all([
        getTodayPunches(employee.id),
        getCurrentStatus(employee.id),
      ]);
      setTodayPunches(punches);
      setIsPunchedIn(status.is_punched_in);
    } catch {
      // silent
    }
  }, [employee.id]);

  useEffect(() => {
    loadData();
  }, [loadData]);

  const handlePunchIn = async () => {
    setLoading(true);
    try {
      await punchIn(employee.id);
      await loadData();
    } catch (e: any) {
      Alert.alert("Error", e.message);
    } finally {
      setLoading(false);
    }
  };

  const handlePunchOut = async () => {
    setLoading(true);
    try {
      await punchOut(employee.id);
      await loadData();
    } catch (e: any) {
      Alert.alert("Error", e.message);
    } finally {
      setLoading(false);
    }
  };

  const handleExit = () => {
    router.replace("/");
  };

  const today = new Date();
  const todayDayIndex = today.getDay();

  // Calculate hours worked today
  let hoursWorked = 0;
  for (let i = 0; i < todayPunches.length - 1; i += 2) {
    const inTime = new Date(todayPunches[i].scan_time).getTime();
    const outTime =
      i + 1 < todayPunches.length
        ? new Date(todayPunches[i + 1].scan_time).getTime()
        : Date.now();
    hoursWorked += (outTime - inTime) / (1000 * 60 * 60);
  }
  // If odd number of punches (currently in), add time since last punch
  if (todayPunches.length % 2 === 1) {
    const lastIn = new Date(todayPunches[todayPunches.length - 1].scan_time).getTime();
    hoursWorked += (Date.now() - lastIn) / (1000 * 60 * 60);
  }

  return (
    <View style={styles.container}>
      {/* Header */}
      <Text style={styles.name}>{employee.full_name}</Text>
      <Text style={styles.date}>{formatDate(today)}</Text>

      {/* Today's punches */}
      <View style={styles.punchLogContainer}>
        <View style={styles.punchLogHeader}>
          <Text style={styles.punchLogHeaderText}>Date</Text>
          <Text style={styles.punchLogHeaderText}>Time</Text>
          <Text style={styles.punchLogHeaderText}></Text>
        </View>
        <ScrollView style={styles.punchLogScroll}>
          {todayPunches.map((p) => (
            <View key={p.id} style={styles.punchLogRow}>
              <Text style={styles.punchLogCell}>
                {formatScanDate(p.scan_date)}
              </Text>
              <Text style={styles.punchLogCell}>{formatTime(p.scan_time)}</Text>
              <Text style={styles.punchLogCell}>{p.punch_type}</Text>
            </View>
          ))}
        </ScrollView>

        <View style={styles.hoursWorkedRow}>
          <Text style={styles.hoursWorkedLabel}>Hrs. Worked</Text>
          <Text style={styles.hoursWorkedValue}>
            {hoursWorked.toFixed(1)} hrs
          </Text>
        </View>
        <View style={styles.todayBar}>
          <Text style={styles.todayText}>Today</Text>
        </View>
      </View>

      {/* Weekly Schedule */}
      <Text style={styles.sectionTitle}>Week Schedule</Text>
      <View style={styles.scheduleTable}>
        <View style={styles.scheduleHeaderRow}>
          <Text style={[styles.scheduleCell, styles.scheduleHeaderCell]}>
            Dept. / Role
          </Text>
          {DAY_LABELS.map((d) => (
            <Text
              key={d}
              style={[styles.scheduleCell, styles.scheduleHeaderCell]}
            >
              {d.slice(0, 3)}
            </Text>
          ))}
        </View>
        <View style={styles.scheduleRow}>
          <Text style={[styles.scheduleCell, styles.scheduleDept]}>
            {employee.department || employee.job_title || "—"}
          </Text>
          {DAYS.map((day) => (
            <Text
              key={`${day}-in`}
              style={[
                styles.scheduleCell,
                styles.scheduleTime,
                day === DAYS[todayDayIndex] && styles.scheduleToday,
              ]}
            >
              {employee.schedule?.[day]?.in || "—"}
            </Text>
          ))}
        </View>
        <View style={styles.scheduleRow}>
          <Text style={[styles.scheduleCell, styles.scheduleDept]}></Text>
          {DAYS.map((day) => (
            <Text
              key={`${day}-out`}
              style={[
                styles.scheduleCell,
                styles.scheduleTime,
                day === DAYS[todayDayIndex] && styles.scheduleToday,
              ]}
            >
              {employee.schedule?.[day]?.out || "—"}
            </Text>
          ))}
        </View>
      </View>

      {/* Action buttons */}
      <View style={styles.buttonRow}>
        <TouchableOpacity
          style={[styles.actionButton, styles.inButton]}
          onPress={handlePunchIn}
          disabled={loading}
        >
          <Text style={styles.actionButtonText}>IN</Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={[styles.actionButton, styles.outButton]}
          onPress={handlePunchOut}
          disabled={loading}
        >
          <Text style={styles.actionButtonText}>OUT</Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={[styles.actionButton, styles.exitButton]}
          onPress={handleExit}
        >
          <Text style={[styles.actionButtonText, styles.exitButtonText]}>
            Exit
          </Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#006400",
    paddingTop: 40,
    paddingHorizontal: 12,
  },
  name: {
    fontSize: 26,
    fontWeight: "bold",
    color: "#fff",
    textAlign: "center",
  },
  date: {
    fontSize: 18,
    color: "#FFD700",
    textAlign: "center",
    marginBottom: 10,
  },
  punchLogContainer: {
    backgroundColor: "#f0f0f0",
    borderWidth: 1,
    borderColor: "#999",
    marginBottom: 8,
    flex: 1,
    maxHeight: 220,
  },
  punchLogHeader: {
    flexDirection: "row",
    backgroundColor: "#ddd",
    borderBottomWidth: 1,
    borderBottomColor: "#999",
    paddingVertical: 4,
    paddingHorizontal: 8,
  },
  punchLogHeaderText: {
    flex: 1,
    fontWeight: "bold",
    fontSize: 13,
    color: "#000",
  },
  punchLogScroll: {
    flex: 1,
    paddingHorizontal: 8,
  },
  punchLogRow: {
    flexDirection: "row",
    paddingVertical: 3,
    borderBottomWidth: 1,
    borderBottomColor: "#e0e0e0",
  },
  punchLogCell: {
    flex: 1,
    fontSize: 13,
    color: "#000",
  },
  hoursWorkedRow: {
    flexDirection: "row",
    justifyContent: "center",
    alignItems: "center",
    paddingVertical: 6,
    backgroundColor: "#e8e8e8",
  },
  hoursWorkedLabel: {
    fontSize: 16,
    fontWeight: "bold",
    color: "#000",
    marginRight: 10,
  },
  hoursWorkedValue: {
    fontSize: 16,
    color: "#000",
  },
  todayBar: {
    backgroundColor: "#FFD700",
    paddingVertical: 4,
    alignItems: "center",
  },
  todayText: {
    fontSize: 16,
    fontWeight: "bold",
    color: "red",
  },
  sectionTitle: {
    fontSize: 14,
    fontWeight: "bold",
    color: "#fff",
    marginBottom: 4,
  },
  scheduleTable: {
    backgroundColor: "#fff",
    borderWidth: 1,
    borderColor: "#999",
    marginBottom: 12,
  },
  scheduleHeaderRow: {
    flexDirection: "row",
    backgroundColor: "#ddd",
    borderBottomWidth: 1,
    borderBottomColor: "#999",
  },
  scheduleRow: {
    flexDirection: "row",
    borderBottomWidth: 1,
    borderBottomColor: "#e0e0e0",
  },
  scheduleCell: {
    flex: 1,
    fontSize: 10,
    paddingVertical: 3,
    paddingHorizontal: 2,
    textAlign: "center",
    color: "#000",
  },
  scheduleHeaderCell: {
    fontWeight: "bold",
    fontSize: 10,
  },
  scheduleDept: {
    fontWeight: "bold",
    textAlign: "left",
    paddingLeft: 4,
  },
  scheduleTime: {
    color: "red",
    fontWeight: "bold",
  },
  scheduleToday: {
    backgroundColor: "#d4edda",
  },
  buttonRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    paddingBottom: 20,
    gap: 10,
  },
  actionButton: {
    flex: 1,
    paddingVertical: 16,
    alignItems: "center",
    borderRadius: 4,
  },
  inButton: {
    backgroundColor: "#fff",
  },
  outButton: {
    backgroundColor: "#fff",
  },
  exitButton: {
    backgroundColor: "#fff",
  },
  actionButtonText: {
    fontSize: 24,
    fontWeight: "bold",
    color: "#000",
  },
  exitButtonText: {
    color: "red",
  },
});
