import { useState } from "react";
import { useParams } from "react-router-dom";
import useChecklists from "./hooks/useChecklists";
import CheckListItem from "./componenets/CheckListItem";
import CheckListStats from "./componenets/CheckListStats";

const CheckListView = () => {
    const { checklistId } = useParams();
    const { checklists, loading, error, toggleChecklistItem, exportChecklist } = useChecklists(checklistId);
    const [filters, setFilters] = useState({
        category: "ALL",
        priority: "ALL",
        status: "ALL",
        search: "",
    });

    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error: {error}</div>;
    if (checklists.length === 0) return <div>No checklists found.</div>;

    const checklist = checklists[0]; // Assuming we are only dealing with one checklist based on the ID


    // Apply filters to checklist items
    const filteredItems = checklist.items.filter((item) => {
        const categoryMatch = filters.category === "ALL" || item.category === filters.category;
        const priorityMatch = filters.priority === "ALL" || item.priority === filters.priority;
        const statusMatch = filters.status === "ALL" || item.status === filters.status;
        const searchMatch = item.description.toLowerCase().includes(filters.search.toLowerCase());
        return categoryMatch && priorityMatch && statusMatch && searchMatch;
    });

    // Group items by category
    const itemsByCategory = filteredItems.reduce((acc, item) => {
        if (!acc[item.category]) acc[item.category] = [];
        acc[item.category].push(item);
        return acc;
    }, {});

    return (
        <div className="max-w-7xl mx-auto p-6">
      {/* Header */}
      <div className="flex justify-between items-start mb-6">
        <div>
          <h1 className="text-3xl font-bold">{checklist.name}</h1>
          {checklist.description && (
            <p className="text-gray-600 mt-2">{checklist.description}</p>
          )}
          <div className="flex gap-2 mt-2">
            {checklist.disaster_type_names.map((name, idx) => (
              <span key={idx} className="px-2 py-1 bg-blue-100 text-blue-700 rounded text-sm">
                {name}
              </span>
            ))}
          </div>
        </div>
        
        <div className="flex gap-2">
          <button
            onClick={exportChecklist}
            className="px-4 py-2 border rounded-lg hover:bg-gray-50"
          >
            📊 Export CSV
          </button>
          <button
            onClick={() => alert("Custom item creation coming soon!")}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            ➕ Add Custom Item
          </button>
        </div>
      </div>
      
      {/* Stats */}
      <ChecklistStats checklist={checklist} />
      
      {/* Filters */}
      <ChecklistFilters filters={filters} onFilterChange={setFilters} />
      
      {/* Items by Category */}
      <div className="space-y-8 mt-6">
        {Object.entries(itemsByCategory).map(([category, items]) => (
          <div key={category}>
            <h2 className="text-xl font-semibold mb-4 capitalize">
              {category.replace('_', ' ')}
              <span className="ml-2 text-gray-500 text-base font-normal">
                ({items.length} items)
              </span>
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {items.map((item) => (
                <CheckListItem
                  key={item.id}
                  item={item}
                  onUpdate={(updatedFields) => toggleChecklistItem(checklist.id, item.id, updatedFields)}
                />
              ))}
            </div>
          </div>
        ))}
        
        {filteredItems.length === 0 && (
          <div className="text-center py-12 text-gray-500">
            No items match your filters
          </div>
        )}
      </div>
    </div>
  );
};

export default CheckListView;