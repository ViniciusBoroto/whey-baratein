// src/components/ThemeToggle.jsx
import { LuMoon, LuSun } from "react-icons/lu";
import { useEffect, useState } from "react";

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
    <button
      onClick={toggleTheme}
      // Using the semantic classes we configured earlier:
      className="flex items-center text-body bg-neutral-primary-soft border border-default hover:bg-neutral-secondary-medium hover:text-heading focus:ring-4 focus:ring-neutral-tertiary-soft shadow-xs font-medium leading-5 rounded-full text-sm px-4 py-2.5 focus:outline-none"
    >
      {isDark ? (
        <LuSun className="inline mr-2" />
      ) : (
        <LuMoon className="inline mr-2" />
      )}
      {isDark ? "Modo escuro" : "Modo claro"}
    </button>
  );
}
