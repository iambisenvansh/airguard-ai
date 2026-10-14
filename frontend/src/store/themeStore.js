import { create } from 'zustand';

export const useThemeStore = create((set) => ({
    isDarkMode: localStorage.getItem('darkMode') === 'true',

    toggleDarkMode: () => {
        set((state) => {
            const newMode = !state.isDarkMode;
            localStorage.setItem('darkMode', newMode);

            // Update document class
            if (newMode) {
                document.documentElement.classList.add('dark');
            } else {
                document.documentElement.classList.remove('dark');
            }

            return { isDarkMode: newMode };
        });
    },

    setDarkMode: (isDark) => {
        localStorage.setItem('darkMode', isDark);
        if (isDark) {
            document.documentElement.classList.add('dark');
        } else {
            document.documentElement.classList.remove('dark');
        }
        set({ isDarkMode: isDark });
    },
}));
