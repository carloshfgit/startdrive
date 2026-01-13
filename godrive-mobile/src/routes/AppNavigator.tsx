import React from 'react';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
// REMOVA ou comente a importação abaixo se não for usar mais nada dela
// import { NavigationContainer } from '@react-navigation/native'; 
import { useAuthStore } from '../stores/useAuthStore';

// Telas
import { LoginScreen } from '../screens/auth/LoginScreen';
import { RegisterScreen } from '../screens/auth/RegisterScreen';
import { AppTabs } from './AppTabs';

const Stack = createNativeStackNavigator();

export const AppNavigator = () => {
  const token = useAuthStore((state) => state.token);
  const isAuthenticated = !!token;

  // REMOVEMOS O <NavigationContainer> DAQUI
  return (
    <Stack.Navigator screenOptions={{ headerShown: false }}>
      {isAuthenticated ? (
        <Stack.Screen name="AppTabs" component={AppTabs} />
      ) : (
        <Stack.Group>
          <Stack.Screen name="Login" component={LoginScreen} />
          <Stack.Screen name="Register" component={RegisterScreen} />
        </Stack.Group>
      )}
    </Stack.Navigator>
  );
};