// Arquivo: src/routes/AppNavigator.tsx

import React from 'react';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { useAuthStore } from '../stores/useAuthStore';

// 📂 Importações atualizadas conforme sua nova estrutura de pastas
import { LoginScreen } from '../screens/auth/LoginScreen';
import { RegisterScreen } from '../screens/auth/RegisterScreen';
import { HomeScreen } from '../screens/student/HomeScreen'; // Assumindo que a Home principal é do aluno por enquanto

// Definição dos tipos das rotas
export type RootStackParamList = {
  Login: undefined;
  Register: undefined;
  Home: undefined;
};

const Stack = createNativeStackNavigator<RootStackParamList>();

export const AppNavigator = () => {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);

  return (
    <Stack.Navigator screenOptions={{ headerShown: false }}>
      {isAuthenticated ? (
        // 🟢 STACK DE APP (Logado vai para Student Home)
        <Stack.Screen name="Home" component={HomeScreen} />
      ) : (
        // 🔴 STACK DE AUTH
        <Stack.Group>
            <Stack.Screen name="Login" component={LoginScreen} />
            <Stack.Screen name="Register" component={RegisterScreen} />
        </Stack.Group>
      )}
    </Stack.Navigator>
  );
};