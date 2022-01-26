<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

// class Tag_User extends Model
// {
//     use HasFactory;

//     public function find()
//     // {
//     //     $tags = Tag::([
//     //         'name' => $request->tag_name,
//     //     ]);
//     }

    
// }

use Illuminate\Database\Eloquent\Relations\Pivot;

class Tag_User extends Pivot
{
    protected $table = "tag_user";
}
