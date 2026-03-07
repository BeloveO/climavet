import { useState } from "react";

/**
 * @typedef {Object} CheckListItemProps
 * @property {Object} item
 * @property {number} item.id
 * @property {string} item.description
 * @property {boolean} item.completed
 * @property {number} checklistId
 * @property {Function} toggleItem
 * @property {Function} onUpdate
 */

const CheckListItem = ({ item, onUpdate }) => {
    const [isExpanded, setIsExpanded] = useState(false);
    const [isEditing, setIsEditing] = useState(false);
    const [editData, setEditData] = useState({
        current_units: item.current_units,
        description: item.description,
        completed: item.completed,
    });

    const getPriorityColor = (priority) => {
        switch (priority) {
            case 'HIGH':
                return 'bg-red-500';
            case 'MEDIUM':
                return 'bg-yellow-500';
            case 'LOW':
                return 'bg-green-500';
            default:
                return 'bg-gray-500';
        }
    };

    const getStatusColor = (status) => {
        switch (status) {
            case 'IN_STOCK':
                return 'bg-green-500';
            case 'OUT_OF_STOCK':
                return 'bg-red-500';
            case 'LOW_STOCK':
                return 'bg-yellow-500';
            case 'NOT_NEEDED':
                return 'bg-gray-500';
            case 'ORDERED':
                return 'bg-blue-500';
            default:
                return 'bg-gray-500';
        }
    };

    const handleSave = () => {
        // Implement save logic here, e.g., call an API to update the item
        onUpdate({
            ...item,
            ...editData,
        });
        setIsEditing(false);
    };

    const percentage = Math.min(100, Math.round((item.current_units / item.required_units) * 100));

    return (
        <div className="border rounded-lg p-4 hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between">
        {/* Left side - Item info */}
        <div className="flex-1">
          <div className="flex items-center gap-3">
            {/* Checkbox */}
            <input
              type="checkbox"
              checked={item.status === 'in_stock'}
              onChange={e => onUpdate({ 
                status: e.target.checked ? 'in_stock' : 'out_of_stock' 
              })}
              className="w-5 h-5"
            />
            
            {/* Name and priority */}
            <div>
              <h3 className="font-semibold text-lg">{item.name}</h3>
              {item.description && (
                <p className="text-sm text-gray-600 mt-1">{item.description}</p>
              )}
            </div>
            
            <span className={`px-2 py-1 rounded text-xs font-medium uppercase ${getPriorityColor(item.priority)}`}>
              {item.priority}
            </span>
          </div>
          
          {/* Progress bar */}
          <div className="mt-3 flex items-center gap-3">
            <div className="flex-1 h-2 bg-gray-200 rounded-full overflow-hidden">
              <div
                className={`h-full ${getStatusColor(item.status)}`}
                style={{ width: `${percentage}%` }}
              />
            </div>
            <span className="text-sm font-medium whitespace-nowrap">
              {item.quantity_current} / {item.quantity_needed} {item.unit}
            </span>
          </div>
        </div>
        
        {/* Right side - Actions */}
        <div className="flex items-center gap-2 ml-4">
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="px-3 py-1 text-sm border rounded hover:bg-gray-50"
          >
            {isExpanded ? 'Less' : 'More'}
          </button>
          
          <button
            onClick={() => setIsEditing(!isEditing)}
            className="px-3 py-1 text-sm bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            {isEditing ? 'Cancel' : 'Edit'}
          </button>
        </div>
      </div>
      
      {/* Expanded details */}
      {isExpanded && !isEditing && (
        <div className="mt-4 pt-4 border-t grid grid-cols-2 gap-4 text-sm">
          <div>
            <span className="font-medium">Location:</span> {item.location || 'Not set'}
          </div>
          <div>
            <span className="font-medium">Supplier:</span> {item.supplier || 'Not set'}
          </div>
          <div>
            <span className="font-medium">Status:</span> {item.status.replace('_', ' ')}
          </div>
          <div>
            <span className="font-medium">Last Checked:</span>{' '}
            {item.last_checked ? new Date(item.last_checked).toLocaleDateString() : 'Never'}
          </div>
          {item.notes && (
            <div className="col-span-2">
              <span className="font-medium">Notes:</span>
              <p className="mt-1 text-gray-600">{item.notes}</p>
            </div>
          )}
        </div>
      )}
      
      {/* Edit form */}
      {isEditing && (
        <div className="mt-4 pt-4 border-t space-y-3">
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-sm font-medium mb-1">
                Current Quantity
              </label>
              <input
                type="number"
                value={editData.quantity_current}
                onChange={e => setEditData(prev => ({ 
                  ...prev, 
                  quantity_current: parseInt(e.target.value) || 0 
                }))}
                className="w-full border rounded p-2"
                min="0"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium mb-1">
                Storage Location
              </label>
              <input
                type="text"
                value={editData.location}
                onChange={e => setEditData(prev => ({ ...prev, location: e.target.value }))}
                className="w-full border rounded p-2"
                placeholder="e.g., Storage Room A, Shelf 3"
              />
            </div>
          </div>
          
          <div>
            <label className="block text-sm font-medium mb-1">
              Supplier
            </label>
            <input
              type="text"
              value={editData.supplier}
              onChange={e => setEditData(prev => ({ ...prev, supplier: e.target.value }))}
              className="w-full border rounded p-2"
              placeholder="Where to purchase this item"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium mb-1">
              Notes
            </label>
            <textarea
              value={editData.notes}
              onChange={e => setEditData(prev => ({ ...prev, notes: e.target.value }))}
              className="w-full border rounded p-2 h-20"
              placeholder="Any additional information..."
            />
          </div>
          
          <div className="flex gap-2">
            <button
              onClick={handleSave}
              className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
            >
              Save Changes
            </button>
            <button
              onClick={() => setIsEditing(false)}
              className="px-4 py-2 border rounded hover:bg-gray-50"
            >
              Cancel
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default CheckListItem;