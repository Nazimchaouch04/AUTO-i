import { useState, useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import axiosClient from '../api/axiosClient';
import { setLoading, setError } from '../store/userSlice';
import { formatCurrency, formatKilometers, formatDate } from '../utils/format';

const MarketplacePage = () => {
  const [listings, setListings] = useState([]);
  const [filters, setFilters] = useState({
    search: '',
    brand: '',
    price_min: '',
    price_max: '',
    year_min: '',
    year_max: '',
  });
  const [pagination, setPagination] = useState({
    count: 0,
    next: null,
    previous: null,
  });

  const dispatch = useDispatch();
  const { loading } = useSelector((state) => state.user);

  useEffect(() => {
    fetchListings();
  }, [filters]);

  const fetchListings = async () => {
    dispatch(setLoading(true));
    try {
      const params = new URLSearchParams();
      
      if (filters.search) params.append('search', filters.search);
      if (filters.brand) params.append('brand', filters.brand);
      if (filters.price_min) params.append('price_min', filters.price_min);
      if (filters.price_max) params.append('price_max', filters.price_max);
      if (filters.year_min) params.append('year_min', filters.year_min);
      if (filters.year_max) params.append('year_max', filters.year_max);

      const response = await axiosClient.get(`/api/marketplace/listings/?${params}`);
      setListings(response.data.results);
      setPagination({
        count: response.data.count,
        next: response.data.next,
        previous: response.data.previous,
      });
    } catch (error) {
      dispatch(setError('Erreur lors du chargement des annonces'));
    } finally {
      dispatch(setLoading(false));
    }
  };

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilters(prev => ({ ...prev, [name]: value }));
  };

  const handleSearch = () => {
    fetchListings();
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-4xl font-bold mb-8 text-center">Marketplace AutoIntel</h1>
        
        {/* Filtres */}
        <div className="bg-gray-800 rounded-lg p-6 mb-8">
          <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-4">
            <input
              type="text"
              name="search"
              placeholder="Rechercher..."
              value={filters.search}
              onChange={handleFilterChange}
              className="bg-gray-700 border border-gray-600 rounded px-4 py-2 text-white"
            />
            
            <select
              name="brand"
              value={filters.brand}
              onChange={handleFilterChange}
              className="bg-gray-700 border border-gray-600 rounded px-4 py-2 text-white"
            >
              <option value="">Toutes marques</option>
              <option value="Renault">Renault</option>
              <option value="Peugeot">Peugeot</option>
              <option value="Volkswagen">Volkswagen</option>
              <option value="BMW">BMW</option>
              <option value="Mercedes">Mercedes</option>
              <option value="Audi">Audi</option>
            </select>
            
            <input
              type="number"
              name="price_min"
              placeholder="Prix min"
              value={filters.price_min}
              onChange={handleFilterChange}
              className="bg-gray-700 border border-gray-600 rounded px-4 py-2 text-white"
            />
            
            <input
              type="number"
              name="price_max"
              placeholder="Prix max"
              value={filters.price_max}
              onChange={handleFilterChange}
              className="bg-gray-700 border border-gray-600 rounded px-4 py-2 text-white"
            />
            
            <input
              type="number"
              name="year_min"
              placeholder="Année min"
              value={filters.year_min}
              onChange={handleFilterChange}
              className="bg-gray-700 border border-gray-600 rounded px-4 py-2 text-white"
            />
            
            <input
              type="number"
              name="year_max"
              placeholder="Année max"
              value={filters.year_max}
              onChange={handleFilterChange}
              className="bg-gray-700 border border-gray-600 rounded px-4 py-2 text-white"
            />
          </div>
          
          <button
            onClick={handleSearch}
            className="mt-4 bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded transition-colors"
          >
            Rechercher
          </button>
        </div>

        {/* Résultats */}
        {loading ? (
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
            <p className="mt-4">Chargement...</p>
          </div>
        ) : (
          <>
            <div className="mb-6 text-gray-400">
              {pagination.count} annonce{pagination.count > 1 ? 's' : ''} trouvée{pagination.count > 1 ? 's' : ''}
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {listings.map((listing) => (
                <div key={listing.id} className="bg-gray-800 rounded-lg overflow-hidden hover:shadow-lg transition-shadow">
                  <div className="h-48 bg-gray-700 flex items-center justify-center">
                    <span className="text-gray-500">Photo</span>
                  </div>
                  
                  <div className="p-6">
                    <h3 className="text-xl font-semibold mb-2">{listing.title}</h3>
                    <div className="text-gray-400 mb-4">
                      {listing.brand} {listing.model} • {listing.year}
                    </div>
                    
                    <div className="flex justify-between items-center mb-4">
                      <span className="text-2xl font-bold text-blue-400">
                        {formatCurrency(listing.price)}
                      </span>
                      <span className="text-gray-400">
                        {formatKilometers(listing.mileage)}
                      </span>
                    </div>
                    
                    <div className="flex gap-2 text-sm text-gray-400">
                      <span>{listing.fuel_type}</span>
                      <span>•</span>
                      <span>{listing.transmission}</span>
                    </div>
                    
                    <div className="mt-4 pt-4 border-t border-gray-700">
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-gray-400">
                          {listing.seller_name}
                        </span>
                        <span className="text-sm text-gray-500">
                          {formatDate(listing.created_at)}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
            
            {listings.length === 0 && (
              <div className="text-center py-12">
                <div className="text-gray-500 text-lg mb-4">
                  Aucune annonce trouvée pour ces critères
                </div>
                <button
                  onClick={() => setFilters({
                    search: '',
                    brand: '',
                    price_min: '',
                    price_max: '',
                    year_min: '',
                    year_max: '',
                  })}
                  className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded transition-colors"
                >
                  Réinitialiser les filtres
                </button>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default MarketplacePage;
