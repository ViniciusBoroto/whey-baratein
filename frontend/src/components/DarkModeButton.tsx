// src/components/ThemeToggle.jsx
import { PiSunBold, PiMoonBold } from "react-icons/pi";
import { useEffect, useState } from "react";
import { SquaredButton } from "./SquaredButton";

export function DarkModeButton() {
  const [isDark, setIsDark] = useState(false);

  // 1. Initialize: Check LocalStorage or System Preference on mount
  useEffect(() => {
    const userStored = localStorage.getItem("theme");
    const systemPrefersDark = window.matchMedia(
      "(prefers-color-scheme: dark)"
    ).matches;

    // If user has a stored preference, use it. Otherwise, use system preference.
    if (userStored === "dark" || (!userStored && systemPrefersDark)) {
      setIsDark(true);
      document.documentElement.classList.add("dark");
    } else {
      setIsDark(false);
      document.documentElement.classList.remove("dark");
    }
  }, []);

  // 2. Toggle Function
  const toggleTheme = () => {
    const newStatus = !isDark;
    setIsDark(newStatus);

    if (newStatus) {
      document.documentElement.classList.add("dark");
      localStorage.setItem("theme", "dark");
    } else {
      document.documentElement.classList.remove("dark");
      localStorage.setItem("theme", "light");
    }
  };

  return (
    <SquaredButton onClick={toggleTheme} className="">
      {isDark ? (
        <PiSunBold className="inline" />
      ) : (
        <PiMoonBold className="inline" />
      )}
    </SquaredButton>
  );
}
