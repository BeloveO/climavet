const CheckListStats = ({ checklist }) => {
    const totalItems = checklist.items.length;
    const completedItems = checklist.items.filter((item) => item.completed).length;
    const progress = totalItems > 0 ? Math.round((completedItems / totalItems) * 100) : 0;

    return (
        <div className="grid grid-cols-4 gap-4 mb-4">
            <div className="bg-white rounded-lg shadow p-4">
                <div className="text-sm text-gray-600">Total Items</div>
                <div className="text-3xl font-bold mt-1">{checklist.total_items}</div>
            </div>
            <div className="bg-green-50 rounded-lg shadow p-4">
                <div className="text-sm text-green-700">In Stock</div>
                <div className="text-3xl font-bold text-green-600 mt-1">
                {checklist.items_in_stock}
                </div>
            </div>
            <div className="bg-red-50 rounded-lg shadow p-4">
                <div className="text-sm text-red-700">Out of Stock</div>
                <div className="text-3xl font-bold text-red-600 mt-1">
                {checklist.items_out_of_stock}
                </div>
            </div>

            {/* Completion bar */}
            <div className="col-span-4 bg-white rounded-lg shadow p-4">
                <div className="flex justify-between items-center mb-2">
                <span className="text-sm font-medium">Overall Completion</span>
                <span className="text-lg font-bold">{checklist.completion_percentage}%</span>
                </div>
                <div className="h-4 bg-gray-200 rounded-full overflow-hidden">
                <div
                    className={`h-full transition-all ${
                    checklist.completion_percentage >= 80 ? 'bg-green-500' :
                    checklist.completion_percentage >= 50 ? 'bg-yellow-500' :
                    'bg-red-500'
                    }`}
                    style={{ width: `${checklist.completion_percentage}%` }}
                />
                <div className="absolute inset-0 flex items-center justify-center text-xs font-semibold text-white">
                    {checklist.completion_percentage}%
                </div>
                </div>
            </div>

            {/* Progress details */}
            <div className="col-span-4 bg-white rounded-lg shadow p-4">
                <div className="text-sm text-gray-600 mb-1">Progress Details</div>
                <div className="text-lg font-bold">
                    {completedItems} of {totalItems} items completed
                </div>
                <div>
                    <div className="h-4 bg-gray-200 rounded-full overflow-hidden mt-2">
                        <div
                        className={`h-full transition-all ${
                            progress >= 80 ? 'bg-green-500' :
                            progress >= 50 ? 'bg-yellow-500' :
                            'bg-red-500'
                        }`}
                        style={{ width: `${progress}%` }}
                        />
                    </div>
                    <div className="text-sm text-gray-600 mt-1">{progress}% completed</div>
                </div>
            </div>
        </div>
    );
};

export default CheckListStats;