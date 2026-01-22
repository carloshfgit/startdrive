/**
 * Storage Utilities
 * 
 * Utilitários para persistência local (AsyncStorage).
 */

import AsyncStorage from '@react-native-async-storage/async-storage';

/**
 * Salva um valor no storage local.
 */
export async function setItem<T>(key: string, value: T): Promise<void> {
    try {
        await AsyncStorage.setItem(key, JSON.stringify(value));
    } catch (error) {
        console.error(`Error saving ${key}:`, error);
    }
}

/**
 * Recupera um valor do storage local.
 */
export async function getItem<T>(key: string): Promise<T | null> {
    try {
        const value = await AsyncStorage.getItem(key);
        return value ? JSON.parse(value) : null;
    } catch (error) {
        console.error(`Error reading ${key}:`, error);
        return null;
    }
}

/**
 * Remove um valor do storage local.
 */
export async function removeItem(key: string): Promise<void> {
    try {
        await AsyncStorage.removeItem(key);
    } catch (error) {
        console.error(`Error removing ${key}:`, error);
    }
}
