import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Layout } from './components/Layout';
import { Dashboard } from './pages/Dashboard';
import { Feed } from './pages/Feed';
import { Analysis } from './pages/Analysis';
import { Recommendation } from './pages/Recommendation';
import { Explainability } from './pages/Explainability';
import { History } from './pages/History';
import { Settings } from './pages/Settings';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="feed" element={<Feed />} />
          <Route path="analysis" element={<Analysis />} />
          <Route path="recommendation" element={<Recommendation />} />
          <Route path="explainability" element={<Explainability />} />
          <Route path="history" element={<History />} />
          <Route path="settings" element={<Settings />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
